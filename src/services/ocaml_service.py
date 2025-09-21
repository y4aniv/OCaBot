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
        Évalue du code OCaml et retourne le résultat dans un environnement sandboxé avec firejail.
        
        Args:
            code: Code OCaml à évaluer
            
        Returns:
            Tuple (succès, résultat) où résultat contient soit la sortie soit l'erreur
        """
        import os
        temp_file_path = None
        
        try:
            logger.info("Début de l'évaluation du code OCaml avec firejail")
            
            with tempfile.NamedTemporaryFile(suffix=".ml", delete=False, mode='w') as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name
            
            firejail_args = [
                "firejail",
                "--quiet",
                "--noroot",
                "--net=none",
                "--private-tmp",
                "--private-dev",
                "--no3d",
                "--nosound",
                "--novideo",
                "--nonewprivs",
                "--seccomp",
                "--caps.drop=all",
                f"--read-only={os.path.dirname(temp_file_path)}",
                "--timeout=00:00:30",
                "--rlimit-cpu=10",
                "--rlimit-as=134217728",
                "--rlimit-nproc=10",
                "sh", "-c",
                f"cat {temp_file_path} | ocaml"
            ]
            
            process = subprocess.Popen(
                firejail_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd="/tmp"
            )
            
            try:
                stdout, stderr = process.communicate(timeout=35)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                logger.warning("Timeout lors de l'évaluation OCaml")
                return False, "Erreur: Timeout - l'exécution a pris trop de temps"
            
            if process.returncode != 0:
                error_msg = stderr.strip() if stderr.strip() else "Erreur inconnue lors de l'exécution"
                logger.warning(f"Erreur firejail/OCaml (code {process.returncode}): {error_msg}")
                return False, error_msg
            
            if stderr and not stderr.startswith("Reading configuration from"):
                if "firejail" not in stderr.lower():
                    logger.warning(f"Avertissement OCaml: {stderr}")
            
            if not stdout.strip():
                return False, "Aucune sortie générée par le code OCaml"
            
            executions = stdout.split("# ")
            executions = [exec.strip() for exec in executions if exec.strip()]
            executions = executions[1:] if len(executions) > 1 else executions
            
            result = "\n\n".join(executions) if executions else stdout.strip()
            logger.info("Évaluation OCaml réussie avec firejail")
            return True, result
                    
        except FileNotFoundError:
            error_msg = "Erreur: firejail n'est pas installé sur le système"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Erreur lors de l'évaluation OCaml: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
        
        finally:
            if temp_file_path:
                try:
                    os.unlink(temp_file_path)
                except:
                    pass