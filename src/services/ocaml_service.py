import tempfile
import subprocess
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

class OCamlService:
    """Service pour l'évaluation de code OCaml."""
    
    @staticmethod
    async def evaluate_code(code: str) -> Tuple[bool, str]:
        """
        Évalue du code OCaml et retourne le résultat.
        
        Args:
            code: Code OCaml à évaluer
            
        Returns:
            Tuple (succès, résultat) où résultat contient soit la sortie soit l'erreur
        """
        try:
            logger.info("Début de l'évaluation du code OCaml")
            
            with tempfile.NamedTemporaryFile(suffix=".ml", delete=False, mode='w') as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            
            with open(temp_file_path, 'r') as file:
                formatted_code = file.read()
            
            with subprocess.Popen(
                ["cat", temp_file_path], 
                stdout=subprocess.PIPE
            ) as cat_process:
                with subprocess.Popen(
                    ["ocaml"], 
                    stdin=cat_process.stdout, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True
                ) as ocaml_process:
                    stdout, stderr = ocaml_process.communicate()
                    
                    if stderr:
                        logger.warning(f"Erreur OCaml: {stderr}")
                        return False, stderr
                    
                    executions = stdout.split("# ")
                    executions = [exec.strip() for exec in executions if exec.strip()]
                    executions = executions[1:] if len(executions) > 1 else executions
                    
                    result = "\n\n".join(executions)
                    logger.info("Évaluation OCaml réussie")
                    return True, result
                    
        except Exception as e:
            error_msg = f"Erreur lors de l'évaluation OCaml: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        
        finally:
            try:
                import os
                os.unlink(temp_file_path)
            except:
                pass