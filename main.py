from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
import logging
from scraping import buscar_odds_bet365, buscar_odds_superbet, buscar_odds_betano, buscar_todas_odds
from surebet import (
    encontrar_surebets, calcular_stakes, projetar_banca, 
    calcular_lucro_esperado, calcular_roi_mensal
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Surebet",
    description="API para encontrar oportunidades de arbitragem em apostas esportivas",
    version="2.0.0"
)

@app.get("/")
def read_root():
    return {
        "mensagem": "API de Surebet v2.0 rodando!", 
        "endpoints": [
            "/odds",
            "/odds/{casa}",
            "/surebets",
            "/calcular-stakes",
            "/projecao",
            "/relatorio-completo"
        ]
    }

@app.get("/odds")
def get_todas_odds():
    """Busca odds de todas as casas disponíveis"""
    try:
        logger.info("Buscando odds de todas as casas...")
        todas_odds = buscar_todas_odds()
        
        total_jogos = sum(len(odds) for odds in todas_odds.values())
        
        return {
            "casas": todas_odds,
            "total_jogos": total_jogos,
            "casas_disponíveis": list(todas_odds.keys())
        }
    except Exception as e:
        logger.error(f"Erro ao buscar odds: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/odds/{casa}")
def get_odds_casa(casa: str):
    """Busca odds de uma casa específica"""
    try:
        casa = casa.lower()
        
        if casa == "bet365":
            odds = buscar_odds_bet365()
        elif casa == "superbet":
            odds = buscar_odds_superbet()
        elif casa == "betano":
            odds = buscar_odds_betano()
        else:
            raise HTTPException(status_code=404, detail="Casa não encontrada. Disponíveis: bet365, superbet, betano")
        
        return {
            "casa": casa,
            "odds": odds,
            "total_jogos": len(odds)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar odds da {casa}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/surebets")
def get_surebets(banca: float = 100.0):
    """Encontra oportunidades de surebet e calcula stakes"""
    try:
        if banca <= 0:
            raise HTTPException(status_code=400, detail="Banca deve ser maior que zero")
        
        logger.info(f"Buscando surebets com banca de R$ {banca}")
        
        # Busca odds de todas as casas
        todas_odds = buscar_todas_odds()
        
        # Encontra surebets comparando casas duas a duas
        surebets = []
        casas = list(todas_odds.keys())
        
        for i in range(len(casas)):
            for j in range(i + 1, len(casas)):
                casa1, casa2 = casas[i], casas[j]
                odds1, odds2 = todas_odds[casa1], todas_odds[casa2]
                
                oportunidades = encontrar_surebets(odds1, odds2)
                
                for op in oportunidades:
                    stake1, stake2 = calcular_stakes(banca, op["odd1"], op["odd2"])
                    
                    if stake1 > 0 and stake2 > 0:
                        lucros = calcular_lucro_esperado(stake1, op["odd1"], stake2, op["odd2"])
                        
                        op.update({
                            "banca_total": banca,
                            "stake1": stake1,
                            "stake2": stake2,
                            "lucro_garantido": lucros["lucro_medio"],
                            "roi_percentual": (lucros["lucro_medio"] / banca) * 100
                        })
                        
                        surebets.append(op)
        
        # Ordena por lucro percentual decrescente
        surebets.sort(key=lambda x: x["lucro_percentual"], reverse=True)
        
        return {
            "surebets": surebets,
            "total_oportunidades": len(surebets),
            "banca_utilizada": banca,
            "melhor_oportunidade": surebets[0] if surebets else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao calcular surebets: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.post("/calcular-stakes")
def calcular_stakes_endpoint(odd1: float, odd2: float, banca: float):
    """Calcula stakes ideais para duas odds específicas"""
    try:
        if odd1 <= 1 or odd2 <= 1:
            raise HTTPException(status_code=400, detail="Odds devem ser maiores que 1")
        if banca <= 0:
            raise HTTPException(status_code=400, detail="Banca deve ser maior que zero")
        
        # Verifica se é uma surebet
        margem = (1/odd1) + (1/odd2)
        
        if margem >= 1:
            return {
                "erro": "Não é uma surebet válida",
                "margem": round(margem, 4),
                "explicacao": "A soma das probabilidades implícitas é >= 1"
            }
        
        stake1, stake2 = calcular_stakes(banca, odd1, odd2)
        lucros = calcular_lucro_esperado(stake1, odd1, stake2, odd2)
        
        return {
            "odd1": odd1,
            "odd2": odd2,
            "banca_total": banca,
            "stake1": stake1,
            "stake2": stake2,
            "margem": round(margem, 4),
            "lucro_garantido": lucros["lucro_medio"],
            "roi_percentual": round((lucros["lucro_medio"] / banca) * 100, 2),
            "lucro_cenario1": lucros["lucro_resultado1"],
            "lucro_cenario2": lucros["lucro_resultado2"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao calcular stakes: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/projecao")
def get_projecao(banca_inicial: float = 400, banca_final: float = 2400, dias: int = 30):
    """Calcula projeção de crescimento de banca"""
    try:
        if banca_inicial <= 0 or banca_final <= banca_inicial or dias <= 0:
            raise HTTPException(
                status_code=400, 
                detail="Parâmetros inválidos: banca_inicial > 0, banca_final > banca_inicial, dias > 0"
            )
        
        retorno_diario = projetar_banca(banca_inicial, banca_final, dias)
        retorno_mensal = ((1 + retorno_diario) ** 30) - 1
        lucro_total = banca_final - banca_inicial
        
        # Simula crescimento dia a dia
        simulacao = []
        banca_atual = banca_inicial
        
        for dia in range(1, min(dias + 1, 31)):  # Limita a 30 dias para não sobrecarregar
            banca_atual *= (1 + retorno_diario)
            simulacao.append({
                "dia": dia,
                "banca": round(banca_atual, 2),
                "lucro_acumulado": round(banca_atual - banca_inicial, 2)
            })
        
        return {
            "banca_inicial": banca_inicial,
            "banca_final": banca_final,
            "dias": dias,
            "retorno_diario_necessario": f"{retorno_diario * 100:.3f}%",
            "retorno_mensal_equivalente": f"{retorno_mensal * 100:.2f}%",
            "lucro_total": lucro_total,
            "roi_total": f"{(lucro_total / banca_inicial) * 100:.2f}%",
            "simulacao_primeiros_30_dias": simulacao
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro na projeção: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/relatorio-completo")
def get_relatorio_completo(banca: float = 1000.0):
    """Gera relatório completo com todas as informações"""
    try:
        if banca <= 0:
            raise HTTPException(status_code=400, detail="Banca deve ser maior que zero")
        
        logger.info("Gerando relatório completo...")
        
        # Busca todas as odds
        todas_odds = buscar_todas_odds()
        
        # Encontra surebets
        surebets = []
        casas = list(todas_odds.keys())
        
        for i in range(len(casas)):
            for j in range(i + 1, len(casas)):
                casa1, casa2 = casas[i], casas[j]
                odds1, odds2 = todas_odds[casa1], todas_odds[casa2]
                
                oportunidades = encontrar_surebets(odds1, odds2)
                
                for op in oportunidades:
                    stake1, stake2 = calcular_stakes(banca, op["odd1"], op["odd2"])
                    
                    if stake1 > 0 and stake2 > 0:
                        lucros = calcular_lucro_esperado(stake1, op["odd1"], stake2, op["odd2"])
                        
                        op.update({
                            "banca_total": banca,
                            "stake1": stake1,
                            "stake2": stake2,
                            "lucro_garantido": lucros["lucro_medio"],
                            "roi_percentual": (lucros["lucro_medio"] / banca) * 100
                        })
                        
                        surebets.append(op)
        
        # Ordena por ROI decrescente
        surebets.sort(key=lambda x: x["roi_percentual"], reverse=True)
        
        # Estatísticas
        total_jogos = sum(len(odds) for odds in todas_odds.values())
        lucro_total_potencial = sum(sb["lucro_garantido"] for sb in surebets)
        roi_medio = sum(sb["roi_percentual"] for sb in surebets) / len(surebets) if surebets else 0
        
        return {
            "resumo": {
                "casas_monitoradas": len(todas_odds),
                "total_jogos": total_jogos,
                "total_surebets": len(surebets),
                "banca_analisada": banca,
                "lucro_total_potencial": round(lucro_total_potencial, 2),
                "roi_medio": round(roi_medio, 2)
            },
            "melhores_oportunidades": surebets[:5],  # Top 5
            "todas_oportunidades": surebets,
            "odds_por_casa": todas_odds,
            "timestamp": "dados atualizados em tempo real"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no relatório completo: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 