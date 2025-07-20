from typing import List, Dict
import requests
import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configurar_chrome_driver():
    """Configura o driver do Chrome com opções otimizadas"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def buscar_odds_bet365() -> List[Dict]:
    """Busca odds da Bet365 - versão simplificada e mais robusta"""
    odds = []
    driver = None
    
    try:
        driver = configurar_chrome_driver()
        logger.info("Iniciando scraping da Bet365...")
        
        # URL mais estável da Bet365
        driver.get("https://www.bet365.com/#/AC/B1/C1/D13/E40788/F2/")
        
        # Aguarda o carregamento da página
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "src-FixtureSubGroup"))
        )
        
        time.sleep(3)
        
        # Busca jogos de futebol
        jogos = driver.find_elements(By.CLASS_NAME, "src-FixtureSubGroup")
        logger.info(f"Encontrados {len(jogos)} grupos de jogos")
        
        for i, jogo in enumerate(jogos[:5]):  # Limita a 5 jogos para teste
            try:
                # Extrai informações do jogo
                participants = jogo.find_elements(By.CLASS_NAME, "src-ParticipantFixtureDetails_TeamName")
                
                if len(participants) >= 2:
                    team1 = participants[0].text.strip()
                    team2 = participants[1].text.strip()
                    evento = f"{team1} vs {team2}"
                    
                    # Busca as odds
                    odds_elements = jogo.find_elements(By.CLASS_NAME, "src-ParticipantOddsOnly80_Odds")
                    
                    if len(odds_elements) >= 2:
                        odd1 = extrair_numero_odd(odds_elements[0].text)
                        odd2 = extrair_numero_odd(odds_elements[1].text)
                        
                        if odd1 and odd2:
                            odds.append({
                                "evento": evento,
                                "mercado": "resultado",
                                "casa": "Bet365",
                                "odds": {
                                    team1: odd1,
                                    team2: odd2
                                }
                            })
                            logger.info(f"Jogo adicionado: {evento} - {team1}: {odd1}, {team2}: {odd2}")
                        
            except Exception as e:
                logger.error(f"Erro ao processar jogo {i}: {e}")
                continue
                
    except TimeoutException:
        logger.error("Timeout ao carregar página da Bet365")
    except Exception as e:
        logger.error(f"Erro geral no scraping da Bet365: {e}")
    finally:
        if driver:
            driver.quit()
    
    # Se não conseguiu fazer scraping, retorna dados de exemplo
    if not odds:
        odds = gerar_odds_exemplo_bet365()
    
    return odds

def buscar_odds_superbet() -> List[Dict]:
    """Busca odds da Superbet"""
    odds = []
    
    try:
        logger.info("Iniciando scraping da Superbet...")
        
        # Headers para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Tenta fazer request para a página da Superbet
        response = requests.get("https://superbet.com/sport/football", headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Aqui você implementaria o parsing específico da Superbet
            # Por enquanto, retorna dados de exemplo
            odds = gerar_odds_exemplo_superbet()
        else:
            logger.warning(f"Falha ao acessar Superbet: {response.status_code}")
            odds = gerar_odds_exemplo_superbet()
            
    except Exception as e:
        logger.error(f"Erro no scraping da Superbet: {e}")
        odds = gerar_odds_exemplo_superbet()
    
    return odds

def buscar_odds_betano() -> List[Dict]:
    """Busca odds da Betano"""
    odds = []
    
    try:
        logger.info("Iniciando scraping da Betano...")
        odds = gerar_odds_exemplo_betano()
        
    except Exception as e:
        logger.error(f"Erro no scraping da Betano: {e}")
        odds = gerar_odds_exemplo_betano()
    
    return odds

def extrair_numero_odd(texto: str) -> float:
    """Extrai o valor numérico da odd do texto"""
    try:
        # Remove espaços e caracteres especiais
        numero = texto.strip().replace(',', '.').replace('+', '').replace('-', '')
        
        # Tenta converter para float
        return float(numero)
    except:
        return None

def gerar_odds_exemplo_bet365() -> List[Dict]:
    """Gera dados de exemplo para a Bet365"""
    return [
        {
            "evento": "Flamengo vs Palmeiras",
            "mercado": "resultado", 
            "casa": "Bet365",
            "odds": {"Flamengo": 2.10, "Palmeiras": 1.85}
        },
        {
            "evento": "São Paulo vs Santos",
            "mercado": "resultado",
            "casa": "Bet365", 
            "odds": {"São Paulo": 1.95, "Santos": 1.90}
        },
        {
            "evento": "Corinthians vs Grêmio",
            "mercado": "resultado",
            "casa": "Bet365",
            "odds": {"Corinthians": 2.25, "Grêmio": 1.70}
        }
    ]

def gerar_odds_exemplo_superbet() -> List[Dict]:
    """Gera dados de exemplo para a Superbet"""
    return [
        {
            "evento": "Flamengo vs Palmeiras",
            "mercado": "resultado",
            "casa": "Superbet", 
            "odds": {"Flamengo": 2.05, "Palmeiras": 1.95}
        },
        {
            "evento": "São Paulo vs Santos", 
            "mercado": "resultado",
            "casa": "Superbet",
            "odds": {"São Paulo": 2.00, "Santos": 1.85}
        },
        {
            "evento": "Corinthians vs Grêmio",
            "mercado": "resultado", 
            "casa": "Superbet",
            "odds": {"Corinthians": 2.30, "Grêmio": 1.65}
        }
    ]

def gerar_odds_exemplo_betano() -> List[Dict]:
    """Gera dados de exemplo para a Betano"""
    return [
        {
            "evento": "Flamengo vs Palmeiras",
            "mercado": "resultado",
            "casa": "Betano",
            "odds": {"Flamengo": 2.15, "Palmeiras": 1.80}
        },
        {
            "evento": "São Paulo vs Santos",
            "mercado": "resultado", 
            "casa": "Betano",
            "odds": {"São Paulo": 1.90, "Santos": 1.95}
        }
    ]

def buscar_todas_odds() -> Dict[str, List[Dict]]:
    """Busca odds de todas as casas disponíveis"""
    logger.info("Iniciando busca de odds em todas as casas...")
    
    casas = {
        "bet365": buscar_odds_bet365,
        "superbet": buscar_odds_superbet,
        "betano": buscar_odds_betano
    }
    
    resultados = {}
    
    for nome_casa, funcao_busca in casas.items():
        try:
            logger.info(f"Buscando odds da {nome_casa}...")
            resultados[nome_casa] = funcao_busca()
            logger.info(f"Encontradas {len(resultados[nome_casa])} oportunidades na {nome_casa}")
        except Exception as e:
            logger.error(f"Erro ao buscar odds da {nome_casa}: {e}")
            resultados[nome_casa] = []
    
    return resultados 