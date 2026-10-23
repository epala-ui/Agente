# Insula Immobiliare — Sistema Multi-Agente AI

Sistema di agenti AI specializzati per automatizzare i processi di **Insula Immobiliare**, sviluppato con Claude AI (Anthropic SDK).

---

## Agenti disponibili

### 1. Agente Risposta Clienti
Gestisce le comunicazioni in entrata dai clienti (email, chat, telefono). Risponde in modo professionale, propone passi successivi e gestisce reclami con empatia.

### 2. Agente Descrizioni Immobili
Genera descrizioni commerciali accattivanti per portali immobiliari, social media e brochure. Adatta il tono al tipo di immobile e al canale di pubblicazione.

### 3. Agente Qualificazione Lead
Analizza le informazioni su potenziali clienti e produce un report strutturato con score di qualificazione (Alto/Medio/Basso) e prossimi passi consigliati.

### 4. Agente Ricerca Immobili
Trova gli immobili più adatti alle esigenze del cliente, confrontando criteri di ricerca con il portfolio disponibile e motivando ogni raccomandazione.

### 5. Agente Gestione Appuntamenti
Gestisce prenotazioni, conferme, spostamenti e cancellazioni di visite agli immobili. Genera comunicazioni formali per clienti e promemoria per gli agenti.

### 6. Agente Marketing Expert
Crea contenuti marketing per Instagram, Facebook, LinkedIn, analisi di mercato, strategie di prezzo e campagne promozionali come open house.

---

## Setup

### Prerequisiti
- Python 3.9+
- Chiave API Anthropic ([ottienila qui](https://console.anthropic.com/))

### Installazione

```bash
# Clona il repository
git clone https://github.com/epala-ui/Agente.git
cd Agente

# Installa le dipendenze
pip install -r requirements.txt

# Imposta la chiave API
export ANTHROPIC_API_KEY="la-tua-chiave-api"
```

### Avvio

```bash
python main.py
```

---

## Struttura del progetto

```
Agente/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py              # Classe base con client Anthropic e caching
│   ├── risposta_clienti.py
│   ├── descrizioni_immobili.py
│   ├── qualificazione_lead.py
│   ├── ricerca_immobili.py
│   ├── gestione_appuntamenti.py
│   └── marketing_expert.py
├── data/
│   └── mock_data.json             # Immobili, agenti e slot disponibili
├── main.py                        # CLI interattiva
├── requirements.txt
└── README.md
```

---

## Uso programmatico

```python
from agents import RicercaImmobiliAgent
import json

with open("data/mock_data.json") as f:
    data = json.load(f)

agent = RicercaImmobiliAgent()
risultato = agent.run({
    "criteri": {
        "tipo": "acquisto",
        "budget_max": 700000,
        "zone": ["EUR", "Prati"],
        "locali_min": 3,
        "metratura_min": 90,
        "caratteristiche": ["garage"]
    },
    "immobili": data["immobili"]
})
print(risultato)
```

---

## Ottimizzazione costi

Il sistema usa **prompt caching** Anthropic: il system prompt di ogni agente viene cachato automaticamente, riducendo i costi API fino all'**80%** sulle chiamate ripetute.

---

## Contatti

- **Email**: info@insulaimmobiliare.com
- **Tel**: +39 06 1234 5678
- **Orari**: Lun-Ven 9:00-19:00, Sab 9:00-13:00
