import logging
import sys
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logger(log_level: str = "INFO") -> None:
    """
    Configure le système de logging pour l'application.
    
    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR)
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'ocabot.log'),
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, 'errors.log'),
        maxBytes=5*1024*1024,
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    logger.handlers.clear()
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    
    logging.getLogger('nextcord').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    
    logger.info("Système de logging initialisé")

def get_logger(name: str) -> logging.Logger:
    """
    Obtient un logger avec le nom spécifié.
    
    Args:
        name: Nom du logger
        
    Returns:
        Instance du logger
    """
    return logging.getLogger(name)