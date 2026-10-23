import os
import anthropic

MODEL = "claude-sonnet-4-6"

INSULA_CONTEXT = """Sei un agente specializzato di Insula Immobiliare, una primaria agenzia immobiliare italiana con sede a Roma.
Insula Immobiliare opera dal 2005 nel mercato residenziale e commerciale romano, con un portfolio di immobili di pregio.
I valori aziendali sono: professionalità, trasparenza, attenzione al cliente e conoscenza approfondita del mercato locale.
Comunica sempre in italiano, con tono professionale ma cordiale. Usa il "Lei" formale nelle comunicazioni con i clienti.
Non inventare dati o prezzi che non ti vengono forniti. Se non hai un'informazione, dillo chiaramente e offri di reperirla."""


class BaseAgent:
    def __init__(self, system_prompt: str):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY non trovata. Impostare la variabile d'ambiente prima di eseguire gli agenti."
            )
        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = system_prompt

    def _call(self, user_message: str, extra_context: str = "") -> str:
        content = user_message
        if extra_context:
            content = f"{extra_context}\n\n{user_message}"

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": content}],
        )
        return response.content[0].text

    def run(self, input_data: dict) -> str:
        raise NotImplementedError("Ogni agente deve implementare il metodo run()")
