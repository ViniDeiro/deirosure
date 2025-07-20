from typing import List, Dict, Tuple
import logging

def encontrar_surebets(odds_casa1: List[Dict], odds_casa2: List[Dict]) -> List[Dict]:
    """
    Encontra oportunidades de surebet entre duas casas de apostas.
    Surebet ocorre quando 1/odd1 + 1/odd2 < 1 para resultados opostos.
    """
    oportunidades = []
    
    for evento1 in odds_casa1:
        for evento2 in odds_casa2:
            # Verifica se é o mesmo evento
            if normalizar_nome_evento(evento1["evento"]) == normalizar_nome_evento(evento2["evento"]):
                
                # Para mercados de resultado duplo (vitória de um time vs outro)
                if evento1["mercado"] == "resultado" and evento2["mercado"] == "resultado":
                    oportunidades.extend(
                        verificar_surebet_resultado_duplo(evento1, evento2)
                    )
                
                # Para mercados over/under
                elif evento1["mercado"] == "total_gols" and evento2["mercado"] == "total_gols":
                    oportunidades.extend(
                        verificar_surebet_over_under(evento1, evento2)
                    )
    
    return oportunidades

def normalizar_nome_evento(nome: str) -> str:
    """Normaliza o nome do evento para comparação"""
    return nome.lower().strip().replace(" x ", " vs ").replace("vs", "vs")

def verificar_surebet_resultado_duplo(evento1: Dict, evento2: Dict) -> List[Dict]:
    """Verifica surebets para mercados de resultado (vitória time A vs time B)"""
    oportunidades = []
    
    # Se temos odds para os mesmos times
    for resultado1, odd1 in evento1["odds"].items():
        for resultado2, odd2 in evento2["odds"].items():
            # Verifica se são resultados opostos (diferentes times)
            if resultado1 != resultado2:
                # Calcula se há arbitragem
                margem = (1/float(odd1)) + (1/float(odd2))
                
                if margem < 1.0:  # Existe surebet
                    lucro_percentual = ((1 - margem) / margem) * 100
                    
                    oportunidades.append({
                        "evento": evento1["evento"],
                        "mercado": "resultado",
                        "casa1": evento1["casa"],
                        "resultado1": resultado1,
                        "odd1": float(odd1),
                        "casa2": evento2["casa"], 
                        "resultado2": resultado2,
                        "odd2": float(odd2),
                        "lucro_percentual": round(lucro_percentual, 2),
                        "margem": round(margem, 4)
                    })
    
    return oportunidades

def verificar_surebet_over_under(evento1: Dict, evento2: Dict) -> List[Dict]:
    """Verifica surebets para mercados over/under"""
    oportunidades = []
    
    for linha1, odds1 in evento1["odds"].items():
        for linha2, odds2 in evento2["odds"].items():
            # Verifica se é a mesma linha mas lados opostos
            if linha1 == linha2:
                if "over" in odds1 and "under" in odds2:
                    margem = (1/float(odds1["over"])) + (1/float(odds2["under"]))
                elif "under" in odds1 and "over" in odds2:
                    margem = (1/float(odds1["under"])) + (1/float(odds2["over"]))
                else:
                    continue
                
                if margem < 1.0:
                    lucro_percentual = ((1 - margem) / margem) * 100
                    
                    oportunidades.append({
                        "evento": evento1["evento"],
                        "mercado": f"total_gols_{linha1}",
                        "casa1": evento1["casa"],
                        "casa2": evento2["casa"],
                        "lucro_percentual": round(lucro_percentual, 2),
                        "margem": round(margem, 4)
                    })
    
    return oportunidades

def calcular_stakes(banca: float, odd1: float, odd2: float) -> Tuple[float, float]:
    """
    Calcula as apostas ideais para garantir o mesmo lucro independente do resultado.
    Formula: stake1 = banca / (1 + odd1/odd2), stake2 = banca - stake1
    """
    try:
        stake1 = banca / (1 + (odd1/odd2))
        stake2 = banca - stake1
        
        # Verifica se os stakes são válidos
        if stake1 <= 0 or stake2 <= 0:
            raise ValueError("Stakes inválidos calculados")
            
        return round(stake1, 2), round(stake2, 2)
    except Exception as e:
        logging.error(f"Erro ao calcular stakes: {e}")
        return 0.0, 0.0

def calcular_lucro_esperado(stake1: float, odd1: float, stake2: float, odd2: float) -> Dict:
    """Calcula o lucro esperado para cada resultado"""
    lucro_resultado1 = (stake1 * odd1) - (stake1 + stake2)
    lucro_resultado2 = (stake2 * odd2) - (stake1 + stake2)
    
    return {
        "lucro_resultado1": round(lucro_resultado1, 2),
        "lucro_resultado2": round(lucro_resultado2, 2),
        "lucro_medio": round((lucro_resultado1 + lucro_resultado2) / 2, 2)
    }

def projetar_banca(banca_inicial: float, banca_final: float, dias: int) -> float:
    """Calcula o retorno diário necessário para atingir o objetivo"""
    if banca_inicial <= 0 or banca_final <= banca_inicial or dias <= 0:
        raise ValueError("Parâmetros inválidos para projeção")
    
    return (banca_final / banca_inicial) ** (1/dias) - 1

def calcular_roi_mensal(lucro_total: float, capital_investido: float) -> float:
    """Calcula o ROI mensal"""
    if capital_investido <= 0:
        return 0.0
    return (lucro_total / capital_investido) * 100 