# Surebet Scraper

Projeto para identificar oportunidades de arbitragem (surebet) entre Bet365 e Superbet, calcular stakes e projetar crescimento de banca.

## Como rodar

1. Ative o ambiente virtual:
   ```
   .\venv\Scripts\activate
   ```
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute a API:
   ```
   uvicorn main:app --reload
   ```

## Endpoints

- `/` — Teste da API
- `/odds` — Odds mockadas das casas
- `/surebets?banca=100` — Oportunidades de surebet e stakes sugeridas
- `/projecao?banca_inicial=400&banca_final=2400&dias=30` — Projeção de crescimento de banca

## Observação

O scraping real das odds ainda precisa ser implementado para Bet365 e Superbet. 