import nextcord
from nextcord.ext import commands
import logging
from src.config.messages import Messages
from src.services.ocaml_service import OCamlService
from src.services.mistral_service import MistralService
from src.utils.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

class EvaluateModal(nextcord.ui.Modal):
    """Modal pour l'évaluation de code OCaml."""
    
    def __init__(self, mistral_service: MistralService):
        super().__init__(Messages.EVALUATE_MODAL_TITLE)
        self.mistral_service = mistral_service

        self.code_input = nextcord.ui.TextInput(
            label=Messages.EVALUATE_CODE_LABEL,
            style=nextcord.TextInputStyle.paragraph,
            required=True,
        )
        self.add_item(self.code_input)

    async def callback(self, interaction: nextcord.Interaction):
        """Traite la soumission du modal."""
        try:
            code = self.code_input.value
            await interaction.response.defer()
            
            logger.info(f"Évaluation OCaml demandée par {interaction.user}")
            
            success, result = await OCamlService.evaluate_code(code)
            
            embed = nextcord.Embed(
                title=Messages.EVALUATE_RESULT_TITLE,
                color=0xDF6799,
            )
            
            embed.set_author(
                name="OCaBot", 
                icon_url=interaction.client.user.avatar.url if interaction.client.user.avatar else None
            )
            
            embed.set_footer(
                text=Messages.REQUESTED_BY.format(user=interaction.user), 
                icon_url=interaction.user.avatar.url if interaction.user.avatar else None
            )
            
            embed.timestamp = interaction.created_at
            
            if success:
                if len(result) > 4096:
                    embed.description = Messages.EVALUATE_OUTPUT_TOO_LONG
                else:
                    embed.description = f"```ocaml\n{result}\n```"
            else:
                embed.description = f"```\nErreur:\n{result}\n```"
                embed.color = 0xFF0000 
            
            await interaction.followup.send(embed=embed)
            
            if interaction.guild and success:
                await self._create_discussion_thread(interaction, code, result)
                
        except Exception as e:
            logger.error(f"Erreur lors de l'évaluation: {str(e)}")
            await ErrorHandler.handle_interaction_error(
                interaction, e, Messages.ERROR_EVALUATION
            )
    
    async def _create_discussion_thread(self, interaction: nextcord.Interaction, code: str, output: str):
        """Crée un thread de discussion avec explication Mistral."""
        try:
            channel = interaction.channel
            async for message in channel.history(limit=1):
                if message.author == interaction.client.user and message.embeds:
                    # Créer le thread avec un nom temporaire d'abord
                    thread_name = Messages.EVALUATE_THREAD_NAME.format(
                        username=interaction.user.display_name
                    )
                    thread = await message.create_thread(name=thread_name)
                    await thread.trigger_typing()
                    
                    custom_thread_name = await self.mistral_service.generate_thread_name(code)
                    
                    if custom_thread_name:
                        try:
                            await thread.edit(name=custom_thread_name)
                            logger.info(f"Thread renommé: {custom_thread_name}")
                        except Exception as rename_error:
                            logger.warning(f"Impossible de renommer le thread: {rename_error}")

                    await thread.trigger_typing()
                    explanation = await self.mistral_service.explain_ocaml_code(code, output)
                    
                    if explanation:
                        chunks = MistralService.split_message(explanation)
                        for chunk in chunks:
                            await thread.send(chunk)
                    else:
                        await thread.send(Messages.ERROR_MISTRAL_RESPONSE)
                    
                    break
                    
        except Exception as e:
            ErrorHandler.log_service_error("Thread Creation", e, f"User: {interaction.user}")

class OCamlCog(commands.Cog):
    """Cog pour les fonctionnalités OCaml."""
    
    def __init__(self, bot, mistral_service: MistralService):
        self.bot = bot
        self.mistral_service = mistral_service
        logger.info("OCamlCog initialisé")
    
    @nextcord.slash_command(name="evaluate", description="Évaluer du code OCaml dans un environnement sécurisé")
    async def evaluate(self, interaction: nextcord.Interaction):
        """Commande pour évaluer du code OCaml."""
        try:
            logger.info(f"Commande evaluate ouverte par {interaction.user}")
            modal = EvaluateModal(self.mistral_service)
            await interaction.response.send_modal(modal)
            
        except Exception as e:
            await ErrorHandler.handle_interaction_error(interaction, e)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Gère les mentions du bot dans les threads OCaml."""
        if message.author == self.bot.user:
            return
        
        if self.bot.user in message.mentions:
            if (hasattr(message.channel, 'parent') and 
                hasattr(message.channel, 'owner') and 
                message.channel.owner == self.bot.user):
                await self._handle_thread_mention(message)
    
    async def _handle_thread_mention(self, message):
        """Gère une mention dans un thread OCaml."""
        try:
            await message.channel.trigger_typing()
            
            thread_history = []
            async for msg in message.channel.history(limit=50, oldest_first=True):
                if msg.content.strip():
                    author_name = "Utilisateur" if msg.author != self.bot.user else "OCaBot"
                    thread_history.append(f"{author_name}: {msg.content}")
            
            context = "\n".join(thread_history[-20:])
            
            response = await self.mistral_service.generate_response(context, message.content)
            
            if response:
                chunks = MistralService.split_message(response)
                for chunk in chunks:
                    await message.reply(chunk)
            else:
                await message.reply(Messages.ERROR_MISTRAL_RESPONSE)
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement de mention: {str(e)}")
            await ErrorHandler.handle_message_error(message, e)

def setup(bot):
    """Fonction requise pour charger le cog."""
    pass