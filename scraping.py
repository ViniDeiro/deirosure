from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def buscar_odds_bet365() -> List[Dict]:
    odds = []
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get("https://www.bet365.bet.br/#/AS/B1/")
        print("Aguardando blocos de jogos aparecerem...")
        # Espera até que pelo menos um bloco de jogo apareça
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.cpm-MarketFixtureContainer'))
        )
        time.sleep(2)
        # Rola a página para baixo para carregar mais jogos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        blocos = driver.find_elements(By.CSS_SELECTOR, '.cpm-MarketFixtureContainer')
        print(f"Encontrou {len(blocos)} blocos de jogos na página.")
        for bloco in blocos[:10]:  # Limita para até 10 jogos para teste
            try:
                times = bloco.find_elements(By.CSS_SELECTOR, '.cpm-ParticipantFixtureDetailsSoccer_TeamContainer')
                if len(times) == 2:
                    time_a = times[0].text.strip()
                    time_b = times[1].text.strip()
                    nome_evento = f"{time_a} x {time_b}"
                else:
                    nome_evento = "Jogo não identificado"
                print(f"Jogo: {nome_evento}")
                # Buscar odds (exemplo: odds principais)
                odds_valores = bloco.find_elements(By.CSS_SELECTOR, '.srb-ParticipantOddsOnly_Odds')
                odds_dict = {}
                if len(odds_valores) >= 2:
                    odds_dict[time_a] = odds_valores[0].text.strip()
                    odds_dict[time_b] = odds_valores[1].text.strip()
                print(f"Odds encontradas: {odds_dict}")
                if odds_dict:
                    odds.append({
                        "evento": nome_evento,
                        "mercado": "1X2",
                        "casa": "Bet365",
                        "odds": odds_dict
                    })
            except Exception as e:
                print(f"Erro ao processar bloco: {e}")
        driver.quit()
    except Exception as e:
        print(f"Erro geral no scraping: {e}")
        driver.quit()
    return odds

# Função mock para buscar odds da Superbet
def buscar_odds_superbet() -> List[Dict]:
    # Aqui entrará o scraping real
    return [
        {"evento": "Time A x Time B", "mercado": "1X2", "casa": "Superbet", "odds": {"A": 2.2, "B": 1.7}},
    ] 