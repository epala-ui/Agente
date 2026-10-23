#!/usr/bin/env python3
"""CLI interattiva per il sistema multi-agente Insula Immobiliare."""

import json
import os
import sys
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "mock_data.json"


def load_mock_data() -> dict:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def check_api_key():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nERRORE: Variabile d'ambiente ANTHROPIC_API_KEY non impostata.")
        print("   Impostala con: export ANTHROPIC_API_KEY='la-tua-chiave'")
        sys.exit(1)


def demo_risposta_clienti(data: dict):
    from agents import RispostaClientiAgent
    agent = RispostaClientiAgent()
    print("\n--- AGENTE RISPOSTA CLIENTI ---")
    result = agent.run({
        "messaggio": "Salve, ho visto il vostro annuncio del trilocale ai Parioli. "
                     "Potreste darmi maggiori informazioni sul prezzo e sulla disponibilità? "
                     "Sono interessato anche a sapere se è possibile visitarlo questo weekend.",
        "canale": "email",
        "nome_cliente": "Sig. Bianchi"
    })
    print(result)


def demo_descrizioni_immobili(data: dict):
    from agents import DescrizioniImmobiliAgent
    agent = DescrizioniImmobiliAgent()
    immobile = data["immobili"][3]
    print("\n--- AGENTE DESCRIZIONI IMMOBILI ---")
    print(f"Immobile: {immobile['titolo']}\n")
    result = agent.run({"immobile": immobile, "tipo_output": "portale"})
    print(result)


def demo_qualificazione_lead(data: dict):
    from agents import QualificazioneLeadAgent
    agent = QualificazioneLeadAgent()
    print("\n--- AGENTE QUALIFICAZIONE LEAD ---")
    result = agent.run({
        "informazioni": (
            "Nome: Famiglia Marini (coppia 35-38 anni, un figlio di 5 anni)\n"
            "Contatto: via form del sito, interessati all'acquisto\n"
            "Zona desiderata: preferibilmente EUR o zone con buone scuole\n"
            "Immobile cercato: almeno 3 locali, preferibilmente con giardino o terrazza\n"
            "Budget dichiarato: 'intorno ai 600-700k'\n"
            "Tempistica: 'vorremmo trovare qualcosa entro l'estate'\n"
            "Situazione attuale: in affitto, contratto scade luglio 2027"
        ),
        "fonte": "sito web",
        "note_agente": "Cliente molto motivato, ha chiamato anche telefonicamente"
    })
    print(result)


def demo_ricerca_immobili(data: dict):
    from agents import RicercaImmobiliAgent
    agent = RicercaImmobiliAgent()
    print("\n--- AGENTE RICERCA IMMOBILI ---")
    result = agent.run({
        "criteri": {
            "tipo": "acquisto",
            "budget_max": 750000,
            "zone": ["EUR", "Prati", "Parioli"],
            "locali_min": 3,
            "metratura_min": 90,
            "caratteristiche": ["garage", "ascensore"]
        },
        "immobili": data["immobili"]
    })
    print(result)


def demo_gestione_appuntamenti(data: dict):
    from agents import GestioneAppuntamentiAgent
    agent = GestioneAppuntamentiAgent()
    immobile = data["immobili"][0]
    print("\n--- AGENTE GESTIONE APPUNTAMENTI ---")
    result = agent.run({
        "azione": "prenota",
        "immobile": immobile,
        "cliente": {
            "nome": "Dott. Alessandro Greco",
            "email": "a.greco@email.com",
            "telefono": "+39 333 1234567"
        },
        "slot_preferiti": ["2026-11-04 mattina", "2026-11-05 qualsiasi ora"],
        "slot_disponibili": data["slot_appuntamenti"]
    })
    print(result)


def demo_marketing_expert(data: dict):
    from agents import MarketingExpertAgent
    agent = MarketingExpertAgent()
    immobile = data["immobili"][1]
    print("\n--- AGENTE MARKETING EXPERT ---")
    result = agent.run({
        "tipo_contenuto": "post_instagram",
        "immobile": immobile,
        "obiettivo": "generare contatti qualificati per acquisto villa",
        "note_aggiuntive": "Puntare su lifestyle, privacy e lusso. Target: famiglie benestanti 40-55 anni."
    })
    print(result)


MENU_ITEMS = [
    ("Agente Risposta Clienti", demo_risposta_clienti),
    ("Agente Descrizioni Immobili", demo_descrizioni_immobili),
    ("Agente Qualificazione Lead", demo_qualificazione_lead),
    ("Agente Ricerca Immobili", demo_ricerca_immobili),
    ("Agente Gestione Appuntamenti", demo_gestione_appuntamenti),
    ("Agente Marketing Expert", demo_marketing_expert),
]


def run_all(data: dict):
    for nome, fn in MENU_ITEMS:
        fn(data)
        print("\n" + "=" * 60 + "\n")


def print_menu():
    print("\n" + "=" * 60)
    print("   INSULA IMMOBILIARE — Sistema Multi-Agente AI")
    print("=" * 60)
    for i, (nome, _) in enumerate(MENU_ITEMS, 1):
        print(f"  {i}. {nome}")
    print(f"  {len(MENU_ITEMS) + 1}. Esegui tutti gli agenti in sequenza")
    print("  0. Esci")
    print("=" * 60)


def main():
    check_api_key()
    data = load_mock_data()

    while True:
        print_menu()
        try:
            scelta = input(f"\nScegli un agente (0-{len(MENU_ITEMS) + 1}): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nArrivederci!")
            break

        if scelta == "0":
            print("\nArrivederci!")
            break
        elif scelta == str(len(MENU_ITEMS) + 1):
            run_all(data)
        elif scelta.isdigit() and 1 <= int(scelta) <= len(MENU_ITEMS):
            idx = int(scelta) - 1
            nome, fn = MENU_ITEMS[idx]
            print(f"\nAvvio: {nome}...")
            try:
                fn(data)
            except Exception as e:
                print(f"\nERRORE: {e}")
        else:
            print("Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()
