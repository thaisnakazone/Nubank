<h2 align="center"> 🟣 Nubank: Avaliação de Negócios e Análise Preditiva 🟣 </h2>

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.10+-blue)

## 📌 Sobre o Projeto

Este repositório documenta uma análise avançada focada no ecossistema do Nubank. O objetivo principal é extrair e identificar problemas e oportunidades de negócio a partir de fontes de dados públicos (dados macroeconômicos, balanços financeiros, sentimento do consumidor, etc.).

Através de análises preditivas e modelagem, o projeto busca avaliar a saúde financeira e o direcionamento estratégico da empresa, culminando em uma apresentação gerencial com foco em tomadas de decisão.

---

## 🗺️ Guia Visual do Repositório

![Guia do Repositório](<assets/guia o que cada pasta faz.png>)

## 📂 Estrutura do Repositório

A arquitetura foi desenhada para garantir a reprodutibilidade da análise, separando dados brutos da experimentação e do código final:

```text
├── data/
│   ├── processed/          # Dados limpos e tratados para modelagem
│   └── raw/                # Dados originais e extrações (imutáveis)
├── notebooks/              # Explorações e testes de hipóteses (.ipynb)
├── reports/                # Apresentação final e dashboards exportados
├── src/                    # Scripts em Python consolidados
│   ├── data_collection.py  # Automações e web scraping (ex: Reclame Aqui)
│   ├── feature_engineering.py
│   ├── modeling.py         # Algoritmos de regressão e forecast
│   └── visualization.py    # Geração de gráficos para a apresentação
├── .gitignore              
├── README.md               
└── requirements.txt        # Bibliotecas necessárias (pandas, scikit-learn, etc.)
```

## 👥 Equipe & Divisão de Responsabilidades  

O pipeline de dados foi estruturado estrategicamente para cobrir **toda a esteira do projeto**, desde a coleta até a geração de insights estratégicos:

### 🔹 Pessoa 1 — Data Engineer  

- Coleta de dados (balanço patrimonial + dados macroeconômicos)  
- Limpeza e tratamento inicial  
- Organização estrutural dos arquivos na pasta `/data`  

### 🔹 Pessoa 2 — Feature Engineer  

- Criação de métricas financeiras  
- Transformações e normalizações  
- Desenvolvimento de variáveis derivadas para enriquecer as análises  

### 🔹 Pessoa 3 — Modelagem  

- Desenvolvimento de modelos preditivos (Regressão e Forecast)  
- Construção de cenários  
- Simulações e análises estatísticas  

### 🔹 Pessoa 4 — Visualização & Business Insights  

- Construção de dashboards  
- Análise estratégica do negócio  
- Elaboração do relatório e apresentação final  

---

## 👤 Integrantes  

- **Thiago Teles**  
- **Paulo Futagawa**  
- **Thaís Nakazone**  
- **Felipe Tavares**  

## 🔄 Fluxo de Trabalho (Code Review)

Nenhum código vai direto para a branch principal.

Fluxo padrão:

- Criar uma **branch** para sua tarefa
- Abrir um **Pull Request (PR)**  
- Passar por **Code Review** de pelo menos um integrante antes do merge  

Esse processo garante organização, qualidade e colaboração no projeto.

## ⚙️ Como Reproduzir o Ambiente

Siga os passos abaixo para configurar o projeto localmente:

### 📥 1. Clone o repositório

```bash
git clone https://github.com/telesvfx/nubank.git
cd nubank
```

## 🐍 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
```

## Ativação no Windows

```bash
.venv\Scripts\activate
```

## 📦 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 📄 Licença

Este projeto está distribuído sob a **Licença MIT**.

Para mais detalhes sobre permissões, limitações e responsabilidades, consulte o arquivo `LICENSE` presente neste repositório.
