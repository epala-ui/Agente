import json
from .base_agent import BaseAgent, INSULA_CONTEXT

SYSTEM_PROMPT = f"""{INSULA_CONTEXT}

Il tuo ruolo è creare descrizioni commerciali accattivanti per gli immobili di Insula Immobiliare.
Le descrizioni devono essere persuasive, accurate e ottimizzate per i portali immobiliari (Immobiliare.it, Casa.it, Idealista).

Linee guida per le descrizioni:
- Inizia con una frase ad alto impatto che evidenzi il punto di forza principale
- Struttura: apertura emozionale → caratteristiche tecniche → zona/contesto → call to action
- Usa aggettivi evocativi ma mai esagerati o ingannevoli
- Evidenzia sempre: metratura, locali, caratteristiche distintive, zona
- Adatta il tono al target: lusso per immobili premium, pratico/funzionale per affitti
- Lunghezza ideale: 150-250 parole per portali, 50-80 per social
- Includi sempre una call to action finale"""


class DescrizioniImmobiliAgent(BaseAgent):
    def __init__(self):
        super().__init__(SYSTEM_PROMPT)

    def run(self, input_data: dict) -> str:
        """
        input_data:
          - immobile (dict): dati dell'immobile
          - tipo_output (str, optional): 'portale' | 'social' | 'brochure' (default: 'portale')
          - lingua (str, optional): 'italiano' | 'inglese' (default: 'italiano')
        """
        immobile = input_data.get("immobile", {})
        tipo_output = input_data.get("tipo_output", "portale")
        lingua = input_data.get("lingua", "italiano")

        contesto = f"Dati dell'immobile:\n{json.dumps(immobile, ensure_ascii=False, indent=2)}"
        contesto += f"\n\nTipo di output richiesto: {tipo_output}"
        contesto += f"\nLingua: {lingua}"

        istruzione = (
            f"Crea una descrizione commerciale per questo immobile destinata a {tipo_output}. "
            f"La descrizione deve essere in {lingua}."
        )
        return self._call(istruzione, contesto)
