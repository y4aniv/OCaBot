"""Messages et textes utilisés par le bot"""

class Messages:
    PING_TITLE = "Pong! 🏓"
    PING_DESCRIPTION = "Latence : {latency:.2f} ms"
    
    EVALUATE_MODAL_TITLE = "Évaluer du code OCaml"
    EVALUATE_CODE_LABEL = "Code OCaml"
    EVALUATE_RESULT_TITLE = "Évaluation du code OCaml"
    EVALUATE_OUTPUT_TOO_LONG = "Sortie trop longue... Essayez de simplifier votre code ou de l'exécuter localement. (Maximum 4096 caractères)"
    EVALUATE_THREAD_NAME = "Discussion OCaml - {username}"
    
    ERROR_GENERAL = "Désolé, j'ai rencontré une erreur. 🤖"
    ERROR_EVALUATION = "Erreur lors de l'évaluation du code OCaml."
    ERROR_THREAD_CREATION = "Erreur lors de la création du thread de discussion."
    ERROR_MISTRAL_RESPONSE = "Erreur lors de la génération de la réponse."
    
    BOT_ONLINE = "OCaBot est en ligne ({bot_user})"
    BOT_SYSTEM_PROMPT = "Tu es OCaBot, un assistant spécialisé en OCaml. Tu aides les utilisateurs avec leurs questions sur le code OCaml. Réponds de manière concise et utile en français."
    
    REQUESTED_BY = "Demandé par {user}"