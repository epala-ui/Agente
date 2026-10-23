import json
from .base_agent import BaseAgent, INSULA_CONTEXT

SYSTEM_PROMPT = f"""{INSULA_CONTEXT}

Sei l'esperto di marketing di Insula Immobiliare. La tua specializzazione è creare strategie e contenuti marketing per immobili e per il brand aziendale.

Le tue competenze includono:
- **Social Media**: contenuti ottimizzati per Instagram, Facebook, LinkedIn con hashtag e copy efficaci
- **Copywriting**: annunci per portali immobiliari, Google Ads, volantini, brochure
- **Strategia di prezzo**: analisi del mercato locale, posizionamento competitivo, suggerimenti di prezzo
- **Analisi di mercato**: trend del mercato immobiliare romano, analisi zone, comparazione prezzi
- **Campagne promozionali**: open house, campagne stagionali, promozioni speciali
- **Personal branding agenti**: contenuti per valorizzare il profilo degli agenti sui social

Linee guida marketing Insula:
- Brand voice: professionale, competente, rassicurante, locale
- Colori brand: blu navy e oro
- Hashtag principali: #InsulaImmobiliare #RomaCase #ImmobiliRoma #CasaRoma
- Sempre includere call to action chiara
- Per Instagram: max 2200 caratteri, 5-10 hashtag rilevanti
- Per LinkedIn: tono più formale, focus su investimento e dati di mercato
- Per Facebook: tono conversazionale, invita all'engagement"""


class MarketingExpertAgent(BaseAgent):
    def __init__(self):
        super().__init__(SYSTEM_PROMPT)

    def run(self, input_data: dict) -> str:
        """
        input_data:
          - tipo_contenuto (str): 'post_instagram' | 'post_facebook' | 'post_linkedin' |
                                   'annuncio_portale' | 'analisi_mercato' | 'strategia_prezzo' |
                                   'campagna_open_house' | 'brochure'
          - immobile (dict, optional): dati dell'immobile
          - zona (str, optional): zona per analisi di mercato
          - budget_campagna (float, optional): budget disponibile
          - obiettivo (str, optional): obiettivo della campagna
          - note_aggiuntive (str, optional): istruzioni aggiuntive
        """
        tipo_contenuto = input_data.get("tipo_contenuto", "post_instagram")
        immobile = input_data.get("immobile")
        zona = input_data.get("zona", "")
        budget_campagna = input_data.get("budget_campagna")
        obiettivo = input_data.get("obiettivo", "")
        note_aggiuntive = input_data.get("note_aggiuntive", "")

        contesto = f"Tipo di contenuto richiesto: {tipo_contenuto}"
        if immobile:
            contesto += f"\n\nDati immobile:\n{json.dumps(immobile, ensure_ascii=False, indent=2)}"
        if zona:
            contesto += f"\nZona di riferimento: {zona}"
        if budget_campagna:
            contesto += f"\nBudget campagna: €{budget_campagna}"
        if obiettivo:
            contesto += f"\nObiettivo: {obiettivo}"
        if note_aggiuntive:
            contesto += f"\nNote aggiuntive: {note_aggiuntive}"

        tipo_map = {
            "post_instagram": "un post per Instagram",
            "post_facebook": "un post per Facebook",
            "post_linkedin": "un articolo/post per LinkedIn",
            "annuncio_portale": "un annuncio per portali immobiliari",
            "analisi_mercato": "un'analisi del mercato immobiliare",
            "strategia_prezzo": "una strategia di prezzo",
            "campagna_open_house": "una campagna per un open house",
            "brochure": "il testo per una brochure",
        }
        tipo_descrizione = tipo_map.get(tipo_contenuto, tipo_contenuto)

        istruzione = f"Crea {tipo_descrizione} professionale per Insula Immobiliare."
        return self._call(istruzione, contesto)
