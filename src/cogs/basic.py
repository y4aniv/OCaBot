import nextcord
from nextcord.ext import commands
import logging
from src.config.messages import Messages
from src.utils.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

class BasicCog(commands.Cog):
    """Cog pour les commandes de base du bot."""
    
    def __init__(self, bot):
        self.bot = bot
        logger.info("BasicCog initialisé")
    
    @nextcord.slash_command(name="ping", description="Vérifier la latence d'OCaBot")
    async def ping(self, interaction: nextcord.Interaction):
        """Commande ping pour vérifier la latence du bot."""
        try:
            logger.info(f"Commande ping exécutée par {interaction.user}")
            
            latency = self.bot.latency * 1000
            embed = nextcord.Embed(
                title=Messages.PING_TITLE,
                description=Messages.PING_DESCRIPTION.format(latency=latency),
                color=0xDF6799,
            )
            
            embed.set_author(
                name="OCaBot", 
                icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
            )
            
            embed.set_footer(
                text=Messages.REQUESTED_BY.format(user=interaction.user), 
                icon_url=interaction.user.avatar.url if interaction.user.avatar else None
            )
            
            embed.timestamp = interaction.created_at
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await ErrorHandler.handle_interaction_error(interaction, e)

def setup(bot):
    """Fonction requise pour charger le cog."""
    bot.add_cog(BasicCog(bot))