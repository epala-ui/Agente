from .base_agent import BaseAgent, INSULA_CONTEXT

SYSTEM_PROMPT = f"""{INSULA_CONTEXT}

Il tuo ruolo specifico è gestire le comunicazioni con i clienti di Insula Immobiliare.
Rispondi a richieste di informazioni, domande sugli immobili, richieste di appuntamenti e qualsiasi altra comunicazione in entrata.

Linee guida:
- Rispondi sempre in modo professionale e cordiale, usando il "Lei"
- Se il cliente chiede di un immobile specifico, chiedi l'ID o il titolo dell'annuncio se non fornito
- Proponi sempre un passo successivo concreto (appuntamento, invio documentazione, contatto telefonico)
- In caso di reclami, mostra empatia e proponi una soluzione immediata
- Firma sempre come "Il Team di Insula Immobiliare"
- Per email, usa un formato professionale con oggetto, corpo e firma"""


class RispostaClientiAgent(BaseAgent):
    def __init__(self):
        super().__init__(SYSTEM_PROMPT)

    def run(self, input_data: dict) -> str:
        """
        input_data:
          - messaggio (str): il messaggio del cliente
          - canale (str, optional): 'email' | 'chat' | 'telefono' (default: 'chat')
          - nome_cliente (str, optional): nome del cliente se noto
        """
        canale = input_data.get("canale", "chat")
        nome_cliente = input_data.get("nome_cliente", "")
        messaggio = input_data.get("messaggio", "")

        contesto = f"Canale di comunicazione: {canale}"
        if nome_cliente:
            contesto += f"\nNome del cliente: {nome_cliente}"
        contesto += f"\n\nMessaggio del cliente:\n{messaggio}"

        istruzione = f"Prepara una risposta professionale al seguente messaggio ricevuto via {canale}."
        return self._call(istruzione, contesto)
