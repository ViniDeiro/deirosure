from fastapi import FastAPI
from typing import List, Dict
from scraping import buscar_odds_bet365, buscar_odds_superbet
from surebet import encontrar_surebets, calcular_stakes, projetar_banca

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensagem": "API de Surebet rodando!"}

@app.get("/odds")
def get_odds():
    odds_bet365 = buscar_odds_bet365()
    odds_superbet = buscar_odds_superbet()
    return {"bet365": odds_bet365, "superbet": odds_superbet}

@app.get("/surebets")
def get_surebets(banca: float = 100):
    odds_bet365 = buscar_odds_bet365()
    odds_superbet = buscar_odds_superbet()
    oportunidades = encontrar_surebets(odds_bet365, odds_superbet)
    for op in oportunidades:
        stake1, stake2 = calcular_stakes(banca, op["odd1"], op["odd2"])
        op["stake1"] = stake1
        op["stake2"] = stake2
    return {"surebets": oportunidades}

@app.get("/projecao")
def get_projecao(banca_inicial: float = 400, banca_final: float = 2400, dias: int = 30):
    retorno_diario = projetar_banca(banca_inicial, banca_final, dias)
    return {"retorno_diario_necessario": f"{retorno_diario*100:.2f}%"} 