from .base_agent import BaseAgent, INSULA_CONTEXT

SYSTEM_PROMPT = f"""{INSULA_CONTEXT}

Il tuo ruolo è qualificare i lead (potenziali clienti) per Insula Immobiliare.
Devi raccogliere informazioni chiave per capire le esigenze del cliente e valutarne il potenziale.

Quando ti vengono fornite informazioni su un lead, analizza e produci un report strutturato che includa:

1. **Profilo cliente**: chi è, qual è la sua situazione
2. **Esigenze immobiliari**: tipo immobile, zona, metratura, caratteristiche richieste
3. **Budget**: fascia di prezzo per acquisto o affitto
4. **Tempistiche**: urgenza della ricerca
5. **Capacità finanziaria**: mutuo pre-approvato, disponibilità liquida, ecc.
6. **Motivazione**: prima casa, investimento, cambio residenza, ecc.
7. **Score di qualificazione**: Alto / Medio / Basso con motivazione
8. **Prossimi passi consigliati**: azioni concrete da intraprendere

Se mancano informazioni, indica quali domande fare al cliente per completare la qualificazione."""


class QualificazioneLeadAgent(BaseAgent):
    def __init__(self):
        super().__init__(SYSTEM_PROMPT)

    def run(self, input_data: dict) -> str:
        """
        input_data:
          - informazioni (str | dict): informazioni disponibili sul lead
          - fonte (str, optional): da dove proviene il lead
          - note_agente (str, optional): note dell'agente che ha avuto il primo contatto
        """
        informazioni = input_data.get("informazioni", "")
        fonte = input_data.get("fonte", "non specificata")
        note_agente = input_data.get("note_agente", "")

        contesto = f"Fonte del lead: {fonte}"
        if note_agente:
            contesto += f"\nNote dell'agente: {note_agente}"
        contesto += f"\n\nInformazioni disponibili sul lead:\n{informazioni}"

        istruzione = "Analizza le informazioni su questo lead e produci un report di qualificazione completo."
        return self._call(istruzione, contesto)
