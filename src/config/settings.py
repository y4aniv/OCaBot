import os
from typing import Optional
import logging
import dotenv

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    """Configuration centralisée du bot."""
    
    def __init__(self):
        self.BOT_TOKEN = self._get_env_var("BOT_TOKEN")
        self.MISTRAL_API_KEY = self._get_env_var("MISTRAL_API_KEY")
        self.LOG_LEVEL = self._get_env_var("LOG_LEVEL", "INFO")
        
    def _get_env_var(self, var_name: str, default: Optional[str] = None) -> str:
        """Récupère une variable d'environnement avec gestion d'erreur."""
        value = os.getenv(var_name, default)
        if value is None:
            logger.error(f"Variable d'environnement {var_name} manquante")
            raise ValueError(f"Variable d'environnement {var_name} requise")
        return value

config = Config()