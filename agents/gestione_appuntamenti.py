import json
from .base_agent import BaseAgent, INSULA_CONTEXT

SYSTEM_PROMPT = f"""{INSULA_CONTEXT}

Il tuo ruolo è gestire la pianificazione degli appuntamenti per visite agli immobili.

Compiti:
1. Verificare la disponibilità degli slot proposti
2. Proporre slot alternativi se quelli richiesti non sono disponibili
3. Generare messaggi di conferma professionale per il cliente
4. Generare promemoria per l'agente
5. Gestire richieste di spostamento o cancellazione appuntamenti

Informazioni ufficio:
- Indirizzo: Via del Corso 12, 00186 Roma
- Telefono: +39 06 1234 5678
- Email: info@insulaimmobiliare.com
- Orari: Lun-Ven 9:00-19:00, Sab 9:00-13:00"""


class GestioneAppuntamentiAgent(BaseAgent):
    def __init__(self):
        super().__init__(SYSTEM_PROMPT)

    def run(self, input_data: dict) -> str:
        """
        input_data:
          - azione (str): 'prenota' | 'conferma' | 'sposta' | 'cancella' | 'promemoria'
          - immobile (dict): dati dell'immobile
          - cliente (dict): nome, email, telefono del cliente
          - slot_preferiti (list, optional): slot orari preferiti dal cliente
          - slot_disponibili (list): slot disponibili
          - appuntamento_esistente (dict, optional): per spostamento/cancellazione
        """
        azione = input_data.get("azione", "prenota")
        immobile = input_data.get("immobile", {})
        cliente = input_data.get("cliente", {})
        slot_disponibili = input_data.get("slot_disponibili", [])
        slot_preferiti = input_data.get("slot_preferiti", [])
        appuntamento_esistente = input_data.get("appuntamento_esistente", {})

        contesto = f"Azione richiesta: {azione}"
        contesto += f"\n\nDati immobile:\n{json.dumps(immobile, ensure_ascii=False, indent=2)}"
        contesto += f"\n\nDati cliente:\n{json.dumps(cliente, ensure_ascii=False, indent=2)}"

        slot_liberi = [s for s in slot_disponibili if s.get("disponibile", False)]
        contesto += f"\n\nSlot disponibili:\n{json.dumps(slot_liberi, ensure_ascii=False, indent=2)}"

        if slot_preferiti:
            contesto += f"\n\nSlot preferiti dal cliente: {slot_preferiti}"
        if appuntamento_esistente:
            contesto += f"\n\nAppuntamento esistente:\n{json.dumps(appuntamento_esistente, ensure_ascii=False, indent=2)}"

        istruzione = f"Gestisci la richiesta di {azione} per l'appuntamento e genera le comunicazioni necessarie."
        return self._call(istruzione, contesto)
