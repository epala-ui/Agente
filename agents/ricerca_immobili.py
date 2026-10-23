import json
from .base_agent import BaseAgent, INSULA_CONTEXT

SYSTEM_PROMPT = f"""{INSULA_CONTEXT}

Il tuo ruolo è analizzare il portfolio di immobili disponibili e trovare le soluzioni più adatte alle esigenze di un cliente.

Processo di raccomandazione:
1. Analizza i criteri del cliente (budget, zona, tipo, metratura, caratteristiche)
2. Confronta con gli immobili disponibili
3. Seleziona le opzioni più compatibili (max 3)
4. Per ogni immobile consigliato, spiega perché è adatto al cliente
5. Evidenzia eventuali compromessi
6. Ordina le raccomandazioni dalla più alla meno adatta

Formato output:
- Breve riepilogo dei criteri del cliente
- Lista degli immobili consigliati con motivazione
- Eventuali suggerimenti alternativi
- Prossimo passo consigliato"""


class RicercaImmobiliAgent(BaseAgent):
    def __init__(self):
        super().__init__(SYSTEM_PROMPT)

    def run(self, input_data: dict) -> str:
        """
        input_data:
          - criteri (dict): tipo, budget_max, zone, locali_min, metratura_min, caratteristiche
          - immobili (list): lista degli immobili disponibili
        """
        criteri = input_data.get("criteri", {})
        immobili = input_data.get("immobili", [])

        contesto = f"Criteri di ricerca del cliente:\n{json.dumps(criteri, ensure_ascii=False, indent=2)}"
        contesto += f"\n\nImmobili disponibili nel portfolio:\n{json.dumps(immobili, ensure_ascii=False, indent=2)}"

        istruzione = "Analizza i criteri del cliente e il portfolio disponibile, poi fornisci le raccomandazioni più adatte."
        return self._call(istruzione, contesto)
