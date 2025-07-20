# 🎯 Sistema Surebet v2.0

Sistema profissional para identificação automática de oportunidades de arbitragem (surebet) em apostas esportivas, com API REST completa e interface de monitoramento.

## ✨ O que foi corrigido

### 🔧 Principais problemas resolvidos:

1. **❌ Lógica de surebet incorreta** → **✅ Lógica corrigida**
   - **Antes**: Comparava odds do mesmo resultado
   - **Agora**: Compara odds opostas (time A vs time B) corretamente
   - **Fórmula**: Surebet quando `1/odd1 + 1/odd2 < 1`

2. **❌ Dependências faltando** → **✅ Todas instaladas**
   - Adicionado: `webdriver-manager`, `requests`, `beautifulsoup4`, `httpx`
   - Removido: `playwright`, `jinja2` (não utilizados)

3. **❌ Scraping frágil** → **✅ Sistema robusto**
   - Fallback para dados de exemplo quando scraping falha
   - Múltiplas casas de apostas (Bet365, Superbet, Betano)
   - Tratamento adequado de erros

4. **❌ API básica** → **✅ API completa**
   - 7 endpoints profissionais
   - Documentação automática (Swagger)
   - Validação de parâmetros
   - Tratamento de erros

5. **❌ Cálculos básicos** → **✅ Matemática avançada**
   - Cálculo de stakes otimizados
   - Projeções de crescimento de banca
   - ROI e lucros garantidos
   - Simulações detalhadas

## 🚀 Como usar

### 1. Instalação
```bash
# Clone o repositório
git clone <repo-url>
cd surebet-project

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt
```

### 2. Teste o sistema
```bash
# Execute os testes automatizados
python test_surebet.py

# Execute a demonstração interativa
python demo_surebet.py
```

### 3. Inicie a API
```bash
# Inicie o servidor
python main.py
# ou
uvicorn main:app --reload

# Acesse:
# - API: http://localhost:8000
# - Documentação: http://localhost:8000/docs
```

## 📚 Endpoints da API

### 🏠 Principal
- `GET /` - Informações da API

### 📊 Odds
- `GET /odds` - Todas as odds de todas as casas
- `GET /odds/{casa}` - Odds específicas (bet365, superbet, betano)

### 🎯 Surebets
- `GET /surebets?banca=1000` - Encontra oportunidades e calcula stakes
- `POST /calcular-stakes` - Calcula stakes para odds específicas

### 📈 Análises  
- `GET /projecao?banca_inicial=400&banca_final=2400&dias=30` - Projeção de crescimento
- `GET /relatorio-completo?banca=1000` - Relatório detalhado

## 🎮 Exemplos de uso

### Via Python
```python
from scraping import buscar_todas_odds
from surebet import encontrar_surebets, calcular_stakes

# Buscar odds
odds = buscar_todas_odds()

# Encontrar surebets
surebets = encontrar_surebets(odds['bet365'], odds['superbet'])

# Calcular stakes para R$ 1000
for sb in surebets:
    stake1, stake2 = calcular_stakes(1000, sb['odd1'], sb['odd2'])
    print(f"Apostar R$ {stake1} e R$ {stake2}")
```

### Via API
```bash
# Buscar surebets
curl "http://localhost:8000/surebets?banca=1000"

# Calcular stakes específicos
curl -X POST "http://localhost:8000/calcular-stakes" \
     -H "Content-Type: application/json" \
     -d '{"odd1": 2.1, "odd2": 1.95, "banca": 1000}'

# Projeção de crescimento
curl "http://localhost:8000/projecao?banca_inicial=1000&banca_final=2000&dias=30"
```

## 🏗️ Arquitetura

```
📦 surebet-project/
├── 🔧 main.py           # API FastAPI
├── 🕷️ scraping.py       # Scraping das casas
├── 🧮 surebet.py        # Lógica de cálculos
├── 🧪 test_surebet.py   # Testes automatizados
├── 🎮 demo_surebet.py   # Demonstração interativa
├── 📋 requirements.txt  # Dependências
└── 📖 README.md         # Documentação
```

### 🎯 Módulos principais:

- **`scraping.py`**: Busca odds das casas de apostas
- **`surebet.py`**: Detecta arbitragens e calcula stakes
- **`main.py`**: API REST com todos os endpoints
- **`test_surebet.py`**: Suite de testes completa
- **`demo_surebet.py`**: Demonstração interativa

## 🧮 Como funciona uma Surebet

### Conceito
Uma surebet (arbitragem) ocorre quando é possível apostar em todos os resultados possíveis de um evento e garantir lucro independente do resultado.

### Exemplo prático:
```
Jogo: Flamengo vs Palmeiras

Casa A: Flamengo @ 2.10, Palmeiras @ 1.85
Casa B: Flamengo @ 1.95, Palmeiras @ 2.05

Surebet encontrada:
- Apostar em Flamengo na Casa A (2.10)
- Apostar em Palmeiras na Casa B (2.05)

Margem: 1/2.10 + 1/2.05 = 0.963 < 1.0 ✅

Com R$ 1000:
- R$ 493.98 em Flamengo @ 2.10
- R$ 506.02 em Palmeiras @ 2.05
- Lucro garantido: R$ 37.35 (3.73%)
```

## 📊 Funcionalidades avançadas

### 🎯 Detecção automática
- ✅ Monitora múltiplas casas simultaneamente
- ✅ Identifica oportunidades em tempo real  
- ✅ Calcula stakes otimizados automaticamente
- ✅ Ordena por ROI decrescente

### 📈 Análises financeiras
- ✅ Projeções de crescimento de banca
- ✅ Cálculo de ROI mensal/anual
- ✅ Simulações de cenários
- ✅ Relatórios detalhados

### 🛡️ Robustez
- ✅ Fallback para dados de exemplo
- ✅ Tratamento de erros completo
- ✅ Logs detalhados
- ✅ Validação de entrada

## 🔮 Próximos passos

### 🎯 Melhorias recomendadas:

1. **Scraping real mais robusto**
   - Implementar rotating proxies
   - Bypass de detecção de bots
   - Scraping de mais casas

2. **Notificações automáticas**
   - Alertas por email/SMS
   - Webhook para Telegram/Discord
   - Limites de ROI mínimo

3. **Interface web**
   - Dashboard em tempo real
   - Gráficos de performance
   - Histórico de apostas

4. **Machine Learning**
   - Predição de odds
   - Otimização de stakes
   - Análise de padrões

## 🛠️ Tecnologias

- **Python 3.13+**
- **FastAPI** - API REST moderna
- **Selenium** - Web scraping
- **BeautifulSoup** - Parsing HTML
- **Pandas** - Análise de dados
- **Uvicorn** - Servidor ASGI

## 📄 Licença

Este projeto é para fins educacionais. Use com responsabilidade e esteja ciente das regulamentações locais sobre apostas.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**⚠️ Aviso Legal**: Este sistema é apenas para fins educacionais. Apostas envolvem riscos financeiros. Use com responsabilidade e dentro da legalidade local. 