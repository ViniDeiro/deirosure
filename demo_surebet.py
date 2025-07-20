#!/usr/bin/env python3
"""
Script de demonstração do sistema de surebet
Mostra exemplos práticos de como usar o sistema
"""

import json
import time
from typing import Dict, List
from scraping import buscar_todas_odds
from surebet import encontrar_surebets, calcular_stakes, calcular_lucro_esperado, projetar_banca

def print_header(titulo: str):
    """Imprime um cabeçalho formatado"""
    print("\n" + "="*60)
    print(f"🎯 {titulo}")
    print("="*60)

def print_section(titulo: str):
    """Imprime uma seção formatada"""
    print(f"\n📋 {titulo}")
    print("-"*40)

def demonstrar_busca_odds():
    """Demonstra a busca de odds"""
    print_section("Buscando odds das casas de apostas...")
    
    odds = buscar_todas_odds()
    
    print("🏠 Casas monitoradas:")
    for casa, jogos in odds.items():
        print(f"  ✅ {casa.upper()}: {len(jogos)} jogos disponíveis")
        
        if jogos:
            print(f"     📌 Exemplo: {jogos[0]['evento']}")
            for time, odd in jogos[0]['odds'].items():
                print(f"        {time}: {odd}")
    
    return odds

def demonstrar_deteccao_surebets(odds: Dict):
    """Demonstra a detecção de surebets"""
    print_section("Detectando oportunidades de surebet...")
    
    total_surebets = 0
    melhores_oportunidades = []
    
    casas = list(odds.keys())
    
    for i in range(len(casas)):
        for j in range(i + 1, len(casas)):
            casa1, casa2 = casas[i], casas[j]
            odds1, odds2 = odds[casa1], odds[casa2]
            
            print(f"\n🔍 Comparando {casa1.upper()} vs {casa2.upper()}...")
            
            surebets = encontrar_surebets(odds1, odds2)
            
            if surebets:
                total_surebets += len(surebets)
                melhores_oportunidades.extend(surebets)
                
                for sb in surebets:
                    print(f"  🎯 SUREBET ENCONTRADA!")
                    print(f"     Evento: {sb['evento']}")
                    print(f"     {sb['casa1']}: {sb['resultado1']} @ {sb['odd1']}")
                    print(f"     {sb['casa2']}: {sb['resultado2']} @ {sb['odd2']}")
                    print(f"     💰 Lucro garantido: {sb['lucro_percentual']:.2f}%")
            else:
                print(f"  ❌ Nenhuma surebet encontrada")
    
    print(f"\n📊 RESUMO: {total_surebets} surebets encontradas!")
    
    # Ordena por lucro decrescente
    melhores_oportunidades.sort(key=lambda x: x['lucro_percentual'], reverse=True)
    
    return melhores_oportunidades

def demonstrar_calculo_stakes(surebets: List, banca: float = 1000):
    """Demonstra o cálculo de stakes"""
    print_section(f"Calculando stakes para banca de R$ {banca}")
    
    if not surebets:
        print("❌ Nenhuma surebet disponível para calcular stakes")
        return
    
    melhor_surebet = surebets[0]
    
    print(f"🏆 MELHOR OPORTUNIDADE:")
    print(f"   Evento: {melhor_surebet['evento']}")
    print(f"   Lucro esperado: {melhor_surebet['lucro_percentual']:.2f}%")
    print()
    
    stake1, stake2 = calcular_stakes(banca, melhor_surebet['odd1'], melhor_surebet['odd2'])
    lucros = calcular_lucro_esperado(stake1, melhor_surebet['odd1'], stake2, melhor_surebet['odd2'])
    
    print(f"💰 DISTRIBUIÇÃO DA BANCA:")
    print(f"   Apostar R$ {stake1:.2f} em {melhor_surebet['resultado1']} na {melhor_surebet['casa1']}")
    print(f"   Apostar R$ {stake2:.2f} em {melhor_surebet['resultado2']} na {melhor_surebet['casa2']}")
    print(f"   Total investido: R$ {stake1 + stake2:.2f}")
    print()
    
    print(f"🎯 LUCROS GARANTIDOS:")
    print(f"   Se {melhor_surebet['resultado1']} ganhar: R$ {lucros['lucro_resultado1']:.2f}")
    print(f"   Se {melhor_surebet['resultado2']} ganhar: R$ {lucros['lucro_resultado2']:.2f}")
    print(f"   Lucro médio garantido: R$ {lucros['lucro_medio']:.2f}")
    print(f"   ROI: {(lucros['lucro_medio'] / banca) * 100:.2f}%")

def demonstrar_projecoes():
    """Demonstra cálculos de projeção"""
    print_section("Calculando projeções de crescimento...")
    
    cenarios = [
        (1000, 2000, 30, "Conservador"),
        (1000, 3000, 30, "Moderado"), 
        (1000, 5000, 30, "Agressivo")
    ]
    
    for banca_inicial, banca_final, dias, tipo in cenarios:
        retorno_diario = projetar_banca(banca_inicial, banca_final, dias)
        lucro_total = banca_final - banca_inicial
        roi_total = (lucro_total / banca_inicial) * 100
        
        print(f"\n📈 CENÁRIO {tipo.upper()}:")
        print(f"   De R$ {banca_inicial} para R$ {banca_final} em {dias} dias")
        print(f"   Retorno diário necessário: {retorno_diario * 100:.3f}%")
        print(f"   Lucro total: R$ {lucro_total}")
        print(f"   ROI total: {roi_total:.1f}%")

def demonstrar_relatorio_completo():
    """Gera um relatório completo"""
    print_section("Gerando relatório completo...")
    
    # Busca todas as odds
    odds = buscar_todas_odds()
    
    # Conta jogos
    total_jogos = sum(len(jogos) for jogos in odds.values())
    
    # Busca surebets
    all_surebets = []
    casas = list(odds.keys())
    
    for i in range(len(casas)):
        for j in range(i + 1, len(casas)):
            casa1, casa2 = casas[i], casas[j]
            odds1, odds2 = odds[casa1], odds[casa2]
            surebets = encontrar_surebets(odds1, odds2)
            all_surebets.extend(surebets)
    
    all_surebets.sort(key=lambda x: x['lucro_percentual'], reverse=True)
    
    print(f"📊 ESTATÍSTICAS GERAIS:")
    print(f"   Casas monitoradas: {len(odds)}")
    print(f"   Total de jogos: {total_jogos}")
    print(f"   Surebets encontradas: {len(all_surebets)}")
    
    if all_surebets:
        melhor_lucro = all_surebets[0]['lucro_percentual']
        lucro_medio = sum(sb['lucro_percentual'] for sb in all_surebets) / len(all_surebets)
        
        print(f"   Melhor oportunidade: {melhor_lucro:.2f}%")
        print(f"   Lucro médio: {lucro_medio:.2f}%")
        
        print(f"\n🏆 TOP 3 OPORTUNIDADES:")
        for i, sb in enumerate(all_surebets[:3], 1):
            print(f"   {i}. {sb['evento']} - {sb['lucro_percentual']:.2f}%")
    
    return all_surebets

def main():
    """Função principal da demonstração"""
    print_header("DEMONSTRAÇÃO DO SISTEMA SUREBET v2.0")
    
    print("🎮 Esta demonstração mostrará:")
    print("   ✅ Busca de odds em múltiplas casas")
    print("   ✅ Detecção automática de surebets")
    print("   ✅ Cálculo de stakes otimizados")
    print("   ✅ Projeções de crescimento de banca")
    print("   ✅ Relatório completo")
    
    input("\n🚀 Pressione ENTER para começar...")
    
    try:
        # 1. Buscar odds
        odds = demonstrar_busca_odds()
        
        # 2. Detectar surebets
        surebets = demonstrar_deteccao_surebets(odds)
        
        # 3. Calcular stakes
        demonstrar_calculo_stakes(surebets, 1000)
        
        # 4. Projeções
        demonstrar_projecoes()
        
        # 5. Relatório completo
        relatorio = demonstrar_relatorio_completo()
        
        print_header("DEMONSTRAÇÃO CONCLUÍDA")
        print("✅ Sistema testado com sucesso!")
        print("🌐 API disponível em: http://localhost:8000")
        print("📖 Documentação em: http://localhost:8000/docs")
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Configure scraping real das casas")
        print("   2. Implemente notificações automáticas")
        print("   3. Adicione mais casas de apostas")
        print("   4. Configure alertas por ROI mínimo")
        
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()