from mistralai import Mistral
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class MistralService:
    """Service pour l'interaction avec l'API Mistral."""
    
    def __init__(self, api_key: str):
        """
        Initialise le service Mistral.
        
        Args:
            api_key: Clé API Mistral
        """
        self.client = Mistral(api_key)
        logger.info("Service Mistral initialisé")
    
    async def explain_ocaml_code(self, code: str, output: str) -> Optional[str]:
        """
        Génère une explication du code OCaml et de sa sortie.
        
        Args:
            code: Code OCaml source
            output: Sortie de l'évaluation
            
        Returns:
            Explication générée ou None en cas d'erreur
        """
        try:
            messages = [{
                "role": "system",
                "content": "Tu es OCaBot, un assistant spécialisé en OCaml. Tu aides les utilisateurs à comprendre le code OCaml et ses sorties. Réponds de manière concise et utile en français."
            },{
                "role": "system",
                "content": "L'évaluation du code OCaml a été effectuée dans un environnement sandboxé avec firejail pour des raisons de sécurité avec les paramètres suivants: mode silencieux, pas de droits root, pas d'accès réseau, dossier /tmp privé, dossier /dev privé, pas d'accélération 3D, pas d'accès audio, pas d'accès vidéo, pas de nouveaux privilèges, filtrage des appels système, suppression de toutes les capacités, accès en lecture seule au dossier contenant le code, timeout de 30 secondes, limite CPU à 10 secondes, limite mémoire à 128MB et limite du nombre de processus à 10."
            }, {
                "role": "user",
                "content": f"Évalue le code OCaml suivant:\n{code}"
            }, {
                "role": "assistant",
                "content": f"Voici l'évaluation du code OCaml\n: {output}"
            },{
                "role": "user",
                "content": "Explique la sortie de manière simple et concise."
            }]
            
            logger.info("Génération d'explication OCaml via Mistral")
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=messages
            )
            
            explanation = response.choices[0].message.content
            logger.info("Explication générée avec succès")
            return explanation
            
        except Exception as e:
            logger.error(f"Erreur lors de l'appel à Mistral: {str(e)}")
            return None
    
    async def generate_thread_name(self, code: str) -> Optional[str]:
        """
        Génère un nom de thread concis basé sur le code OCaml.
        
        Args:
            code: Code OCaml source
            
        Returns:
            Nom de thread généré ou None en cas d'erreur
        """
        try:
            messages = [{
                "role": "system",
                "content": "Tu es un assistant qui génère des noms de threads concis et descriptifs. Le nom doit faire maximum 50 caractères, être en français et décrire brièvement ce que fait le code OCaml. N'utilise pas de guillemets dans ta réponse, juste le nom du thread."
            }, {
                "role": "user",
                "content": f"Génère un nom de thread concis (max 50 caractères) qui décrit ce code OCaml:\n{code}"
            }]
            
            logger.info("Génération de nom de thread via Mistral")
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=messages
            )
            
            thread_name = response.choices[0].message.content.strip()
            if len(thread_name) > 50:
                thread_name = thread_name[:47] + "..."
            
            logger.info(f"Nom de thread généré: {thread_name}")
            return thread_name
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du nom de thread: {str(e)}")
            return None
    
    async def generate_response(self, context: str, question: str) -> Optional[str]:
        """
        Génère une réponse basée sur le contexte et la question.
        
        Args:
            context: Contexte de la conversation
            question: Question de l'utilisateur
            
        Returns:
            Réponse générée ou None en cas d'erreur
        """
        try:
            messages = [{
                "role": "system",
                "content": "Tu es OCaBot, un assistant spécialisé en OCaml. Tu aides les utilisateurs uniquement avec leurs questions sur le code OCaml. Réponds de manière concise et utile en français."
            }, {
                "role": "user", 
                "content": f"Contexte de la discussion:\n{context}\n\nQuestion actuelle: {question}"
            }]
            
            logger.info("Génération de réponse contextuelle via Mistral")
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=messages
            )
            
            result = response.choices[0].message.content
            logger.info("Réponse générée avec succès")
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors de l'appel à Mistral: {str(e)}")
            return None
    
    @staticmethod
    def split_message(message: str, max_length: int = 2000) -> List[str]:
        """
        Divise un message en chunks pour respecter les limites Discord.
        
        Args:
            message: Message à diviser
            max_length: Taille maximale par chunk
            
        Returns:
            Liste des chunks
        """
        if len(message) <= max_length:
            return [message]
        
        chunks = []
        for i in range(0, len(message), max_length):
            chunks.append(message[i:i+max_length])
        
        logger.info(f"Message divisé en {len(chunks)} chunks")
        return chunks