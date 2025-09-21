import logging
import nextcord
from typing import Optional
from src.config.messages import Messages

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Gestionnaire centralisé des erreurs."""
    
    @staticmethod
    async def handle_interaction_error(interaction: nextcord.Interaction, error: Exception, custom_message: Optional[str] = None) -> None:
        """
        Gère les erreurs d'interaction Discord.
        
        Args:
            interaction: Interaction Discord
            error: Exception survenue
            custom_message: Message personnalisé (optionnel)
        """
        logger.error(f"Erreur d'interaction: {str(error)}", exc_info=True)
        
        message = custom_message or Messages.ERROR_GENERAL
        
        try:
            if interaction.response.is_done():
                await interaction.followup.send(message, ephemeral=True)
            else:
                await interaction.response.send_message(message, ephemeral=True)
        except Exception as e:
            logger.error(f"Impossible d'envoyer le message d'erreur: {str(e)}")
    
    @staticmethod
    async def handle_message_error(message: nextcord.Message, error: Exception, custom_message: Optional[str] = None) -> None:
        """
        Gère les erreurs de message Discord.
        
        Args:
            message: Message Discord
            error: Exception survenue
            custom_message: Message personnalisé (optionnel)
        """
        logger.error(f"Erreur de message: {str(error)}", exc_info=True)
        
        error_message = custom_message or Messages.ERROR_GENERAL
        
        try:
            await message.reply(error_message)
        except Exception as e:
            logger.error(f"Impossible d'envoyer la réponse d'erreur: {str(e)}")
    
    @staticmethod
    def log_service_error(service_name: str, error: Exception, context: Optional[str] = None) -> None:
        """
        Log une erreur de service.
        
        Args:
            service_name: Nom du service
            error: Exception survenue
            context: Contexte additionnel (optionnel)
        """
        context_info = f" - Contexte: {context}" if context else ""
        logger.error(f"Erreur dans {service_name}: {str(error)}{context_info}", exc_info=True)