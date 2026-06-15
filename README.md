<h2 align="center">🟣 Nubank: Avaliação de Negócios e Análise Preditiva 🟣</h2>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Concluído-brightgreen"/>
  <img src="https://img.shields.io/badge/License-MIT-blue"/>
  <img src="https://img.shields.io/badge/Python-3.10+-blue"/>
  <img src="https://img.shields.io/badge/Jupyter-Notebook-orange"/>
</p>

---

## 📌 Sobre o Projeto

Este projeto realiza uma análise completa do ecossistema financeiro do Nubank, combinando **dados regulatórios do Banco Central do Brasil** (Circular BCB 3.930 — Pilar 3) com **dados de sentimento do consumidor** extraídos do Reclame Aqui via web scraping.

O objetivo foi identificar riscos, oportunidades e padrões estratégicos na operação do Nubank, culminando em dashboards interativos e uma apresentação gerencial com foco em tomada de decisão.

---

## 🔍 Metodologia & Análises Realizadas

### 📊 Análise Regulatória (Pilar 3 — BCB 3.930)
- Extração e preprocessamento de 8 trimestres de dados regulatórios (arquivos KM1, OV1, CR1, CR2, MR1)
- Análise de tendência do **Índice de Basileia**
- Monitoramento do crescimento de **RWA (Risk-Weighted Assets)** e spike de **RWA Cambial**
- Construção de pipeline estruturado em Python/Pandas/OpenPyXL com output em Excel multi-abas

### 🗣️ Análise de Reclamações (Reclame Aqui)
- Web scraping automatizado de reclamações do Nubank
- **Clusterização K-Means** para segmentação de perfis de reclamação
- **Regressão linear** sobre complexidade textual das reclamações
- Geração de insights sobre categorias e sazonalidade de reclamações

### 📈 Dashboards & Visualizações
- Dashboard financeiro com indicadores regulatórios e de capital
- Dashboard de reclamações com análise de clusters e tendências
- Relatório executivo consolidado

---

## 📊 Visualização do Dashboard

Abaixo uma prévia do resultado final, com os **cards de indicadores**, botão da **Selic** e gráficos interativos:

![Dashboard](assets/dashboard_preview.png)

---

## 🗺️ Guia Visual do Repositório

![Guia do Repositório](<assets/guia o que cada pasta faz.png>)

## 📂 Estrutura do Repositório

```text
├── data/
│   ├── processed/               # Dados limpos e tratados para modelagem
│   └── raw/                     # Dados originais (imutáveis) — Pilar 3 BCB
├── notebooks/
│   ├── nubank.ipynb             # Análise principal — Pilar 3 & Reclame Aqui
│   ├── analises.ipynb           # Análises complementares
│   └── dashboard.ipynb          # Notebook de geração de dashboards
├── reports/
│   ├── dashboard_financeiro.py  # Indicadores financeiros e regulatórios
│   └── dashboard_reclamacoes.py # Análise de reclamações e clusters
├── src/
│   ├── load_api_to_sqlite.py    # Ingestão via API para SQLite
│   ├── load_csv_to_sqlite.py    # Ingestão de CSVs para SQLite
│   └── load_xlsx_to_sqlite.py   # Ingestão de Excel para SQLite
├── assets/                      # Imagens e recursos visuais
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 👥 Equipe

**Felipe Tavares**
**Paulo Futagawa**
**Thaís Nakazone**
**Thiago Teles**

---

## ⚙️ Como Reproduzir o Ambiente

Siga os passos abaixo para configurar o projeto localmente:

### 1. Clone o repositório
```bash
git clone https://github.com/thaisnakazone/Nubank.git
cd Nubank
```

## 2. Crie e ative o ambiente virtual
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

## 📦 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute os notebooks ou scripts Python

1. `notebooks/nubank.ipynb`
2. `notebooks/dashboard.ipynb`
3. `reports/dashboard_financeiro.py`
4. `reports/dashboard_reclamacoes.py`

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+** — linguagem principal
- **Pandas / NumPy** — manipulação e processamento de dados
- **Scikit-Learn** — K-Means e regressão linear
- **Matplotlib / Seaborn / Plotly** — visualizações
- **OpenPyXL** — leitura e escrita de Excel regulatório
- **SQLite** — armazenamento intermediário
- **Jupyter Notebook** — exploração e apresentação
- **Git / GitHub** — versionamento com fluxo de branches e PRs

---

## 📄 Licença

Este projeto está distribuído sob a **Licença MIT**. Consulte o arquivo `LICENSE` para mais detalhes.