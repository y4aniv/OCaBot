import os
import sys
import asyncio
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config.settings import config
from src.config.messages import Messages
from src.services.mistral_service import MistralService
from src.utils.logger import setup_logger, get_logger
from src.utils.error_handler import ErrorHandler

load_dotenv()

setup_logger(config.LOG_LEVEL)
logger = get_logger(__name__)

class OCaBot(commands.Bot):
    """Classe principale du bot OCaBot."""
    
    def __init__(self):
        """Initialise le bot avec les intents nécessaires."""
        intents = nextcord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.mistral_service = MistralService(config.MISTRAL_API_KEY)
        
        logger.info("OCaBot initialisé")
    
    async def on_ready(self):
        """Événement déclenché quand le bot est prêt."""
        logger.info(Messages.BOT_ONLINE.format(bot_user=self.user))
        
        await self.load_cogs()
        
        try:
            await self.sync_all_application_commands()
            logger.info("Commandes slash synchronisées")
        except Exception as e:
            logger.error(f"Erreur lors de la synchronisation des commandes: {e}")
    
    async def load_cogs(self):
        """Charge tous les cogs du bot."""
        cogs_to_load = [
            'src.cogs.basic',
        ]
        
        for cog_name in cogs_to_load:
            try:
                self.load_extension(cog_name)
                logger.info(f"Cog {cog_name} chargé avec succès")
            except Exception as e:
                logger.error(f"Erreur lors du chargement du cog {cog_name}: {e}")
        
        try:
            from src.cogs.ocaml import OCamlCog
            self.add_cog(OCamlCog(self, self.mistral_service))
            logger.info("OCamlCog chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement d'OCamlCog: {e}")
    
    async def on_command_error(self, ctx, error):
        """Gère les erreurs de commandes."""
        logger.error(f"Erreur de commande: {error}")
        await ErrorHandler.handle_message_error(ctx.message, error)
    
    async def on_application_command_error(self, interaction, error):
        """Gère les erreurs de commandes slash."""
        logger.error(f"Erreur de commande slash: {error}")
        await ErrorHandler.handle_interaction_error(interaction, error)

async def main():
    """Fonction principale d'exécution du bot."""
    try:
        if not config.BOT_TOKEN:
            logger.error("BOT_TOKEN manquant dans les variables d'environnement")
            return
        
        if not config.MISTRAL_API_KEY:
            logger.error("MISTRAL_API_KEY manquant dans les variables d'environnement")
            return
        
        bot = OCaBot()
        
        logger.info("Démarrage d'OCaBot...")
        await bot.start(config.BOT_TOKEN)
        
    except KeyboardInterrupt:
        logger.info("Arrêt du bot demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur critique lors du démarrage: {e}", exc_info=True)
    finally:
        logger.info("OCaBot arrêté")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nArrêt du bot...")
    except Exception as e:
        print(f"Erreur fatale: {e}")
        sys.exit(1)