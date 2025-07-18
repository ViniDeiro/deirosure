from typing import List, Dict, Tuple

def encontrar_surebets(odds1: Dict, odds2: Dict) -> List[Dict]:
    # odds1 e odds2: lista de odds de cada casa
    oportunidades = []
    for odd1 in odds1:
        for odd2 in odds2:
            if odd1["evento"] == odd2["evento"] and odd1["mercado"] == odd2["mercado"]:
                # Exemplo para mercado 1X2 (dois resultados)
                for resultado in odd1["odds"]:
                    if resultado in odd2["odds"]:
                        o1 = odd1["odds"][resultado]
                        o2 = odd2["odds"][resultado]
                        if 1/o1 + 1/o2 < 1:
                            oportunidades.append({
                                "evento": odd1["evento"],
                                "mercado": odd1["mercado"],
                                "casa1": odd1["casa"],
                                "odd1": o1,
                                "casa2": odd2["casa"],
                                "odd2": o2,
                                "lucro_percentual": (1 - (1/o1 + 1/o2)) * 100
                            })
    return oportunidades

def calcular_stakes(banca: float, odd1: float, odd2: float) -> Tuple[float, float]:
    # Divide a banca para garantir lucro
    stake1 = banca / (1 + (odd1/odd2))
    stake2 = banca - stake1
    return round(stake1, 2), round(stake2, 2)

def projetar_banca(banca_inicial: float, banca_final: float, dias: int) -> float:
    # Retorno diário necessário para atingir o objetivo
    return (banca_final / banca_inicial) ** (1/dias) - 1 