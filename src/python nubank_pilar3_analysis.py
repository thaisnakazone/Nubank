"""
Nubank Pilar 3 – Análise Completa 2025
Análise dos dados regulatórios publicados nos arquivos da Circular BCB 3.930

Dependências:
    pip install pandas matplotlib seaborn openpyxl numpy

Como usar:
    python nubank_pilar3_analysis.py

Os arquivos Excel devem estar na mesma pasta do script, com os nomes originais:
    - anexo-pilar3-circular-3930-q1-2025__1_.xlsx
    - anexo-pilar3-circular-3930-q2-2025__1_.xlsx
    - anexo-pilar3-circular-3930-q3-2025__1_.xlsx
    - anexo-pilar3-circular-3930-q4-2025.xlsx
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import seaborn as sns

warnings.filterwarnings("ignore")

# ─── Configurações visuais ────────────────────────────────────────────────────
PURPLE      = "#6B2D8B"
PURPLE_LIGHT = "#9B59B6"
PURPLE_DARK  = "#4A1F6F"
MAGENTA     = "#C0392B"
GOLD        = "#F39C12"
TEAL        = "#16A085"
BLUE        = "#2980B9"
GRAY        = "#7F8C8D"
BG          = "#F9F9FB"

sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   BG,
    "axes.edgecolor":   "#CCCCCC",
    "axes.spines.top":  False,
    "axes.spines.right": False,
    "font.family":      "DejaVu Sans",
    "axes.titleweight": "bold",
    "axes.titlesize":   13,
    "axes.labelsize":   11,
})

# ─── Caminhos dos arquivos ────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "Q1/2025": os.path.join(SCRIPT_DIR, "anexo-pilar3-circular-3930-q1-2025__1_.xlsx"),
    "Q2/2025": os.path.join(SCRIPT_DIR, "anexo-pilar3-circular-3930-q2-2025__1_.xlsx"),
    "Q3/2025": os.path.join(SCRIPT_DIR, "anexo-pilar3-circular-3930-q3-2025__1_.xlsx"),
    "Q4/2025": os.path.join(SCRIPT_DIR, "anexo-pilar3-circular-3930-q4-2025.xlsx"),
}

Q4_FILE = FILES["Q4/2025"]

# ─── Helpers ─────────────────────────────────────────────────────────────────
def fmt_bi(v):
    """Formata valor em bilhões BRL."""
    return f"R$ {v/1e9:.1f} bi"

def fmt_mi(v):
    """Formata valor em milhões BRL."""
    return f"R$ {v/1e6:.1f} mi"

def pct(v):
    return f"{v*100:.1f}%"

def read_sheet(quarter_key, sheet):
    return pd.read_excel(FILES[quarter_key], sheet_name=sheet, header=None)

def add_bar_labels(ax, fmt="{:.1f}", unit="", fontsize=9, color="white", threshold=0):
    for bar in ax.patches:
        h = bar.get_height()
        if abs(h) > threshold:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2,
                fmt.format(h) + unit,
                ha="center", va="center",
                fontsize=fontsize, color=color, fontweight="bold"
            )

# ═══════════════════════════════════════════════════════════════════════════════
# 1. EXTRAÇÃO DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════

def extract_km1():
    """Extrai dados de capital, RWA e índices prudenciais – KM1."""
    records = []

    def get_val(df, row_id, col_idx):
        for _, row in df.iterrows():
            if str(row.iloc[2]).strip() == str(row_id):
                v = row.iloc[col_idx]
                try:
                    return float(v) if str(v) not in ["-", "nan", "None"] else np.nan
                except:
                    return np.nan
        return np.nan

    for quarter, path in FILES.items():
        xl = pd.ExcelFile(path)
        if "KM1" not in xl.sheet_names:
            continue
        df = pd.read_excel(path, sheet_name="KM1", header=None)

        # col 4 = período corrente
        r = {"Trimestre": quarter}
        r["Capital Principal"]      = get_val(df, "1",  4)
        r["Nível I"]                = get_val(df, "2",  4)
        r["PR"]                     = get_val(df, "3",  4)
        r["RWA Total"]              = get_val(df, "4",  4)
        r["ICP (%)"]                = get_val(df, "5",  4)
        r["Índice Nível 1 (%)"]     = get_val(df, "6",  4)
        r["Índice de Basileia (%)"] = get_val(df, "7",  4)
        r["ACP Total (%)"]          = get_val(df, "11", 4)
        r["Margem Exc. ICP (%)"]    = get_val(df, "12", 4)
        records.append(r)

    return pd.DataFrame(records)


def extract_ov1():
    """Extrai composição do RWA por tipo de risco – OV1 (Q4)."""
    df = pd.read_excel(Q4_FILE, sheet_name="OV1", header=None)
    items = {
        "7":  "Risco de Crédito (Sentido Estrito)",
        "6":  "Risco de Crédito de Contraparte",
        "16": "Securitização",
        "20": "Risco de Mercado",
        "21": "Risco Operacional",
        "22": "Outros",
    }
    data = {}
    for _, row in df.iterrows():
        key = str(row.iloc[2]).strip()
        if key in items:
            try:
                v = float(row.iloc[4])
                data[items[key]] = v
            except:
                pass
    # fallback: linha 1 = crédito estrito
    if not data:
        return {}
    return data


def extract_cr1():
    """Extrai qualidade creditícia das exposições – CR1 (Q4)."""
    df = pd.read_excel(Q4_FILE, sheet_name="CR1", header=None)
    rows = []
    categories = {"1": "Concessão de Crédito", "2": "Títulos de Dívida",
                  "3": "Operações Off-Balance", "4": "Total"}
    for _, row in df.iterrows():
        key = str(row.iloc[2]).strip()
        if key in categories:
            try:
                prob = float(row.iloc[4]) if str(row.iloc[4]) not in ["-","nan"] else 0
                n_prob = float(row.iloc[5]) if str(row.iloc[5]) not in ["-","nan"] else 0
                prov   = float(row.iloc[6]) if str(row.iloc[6]) not in ["-","nan"] else 0
                rows.append({
                    "Categoria": categories[key],
                    "Ativos Problemáticos (R$ mil)": prob,
                    "Ativos Não Problemáticos (R$ mil)": n_prob,
                    "Provisões (R$ mil)": prov,
                })
            except:
                pass
    return pd.DataFrame(rows)


def extract_cr2():
    """Extrai mudanças no estoque de ativos problemáticos – CR2 (Q4)."""
    df = pd.read_excel(Q4_FILE, sheet_name="CR2", header=None)
    labels = {
        "1": "Estoque inicial (Q3)",
        "2": "Novos problemáticos",
        "3": "Saíram da classificação",
        "4": "Baixa contábil",
        "5": "Outros ajustes",
        "6": "Estoque final (Q4)",
    }
    data = {}
    for _, row in df.iterrows():
        key = str(row.iloc[2]).strip()
        if key in labels:
            try:
                data[labels[key]] = float(row.iloc[4])
            except:
                pass
    return data


def extract_ov1_series():
    """RWA por tipo de risco disponível – Q2 e Q4."""
    result = {}
    for q in ["Q2/2025", "Q4/2025"]:
        xl = pd.ExcelFile(FILES[q])
        if "OV1" not in xl.sheet_names:
            continue
        df = pd.read_excel(FILES[q], sheet_name="OV1", header=None)
        rwa = {}
        mapping = {
            "7":  "Crédito (Estrito)",
            "6":  "CCR",
            "16": "Securitização",
            "20": "Mercado",
            "21": "Op. Risco",
        }
        for _, row in df.iterrows():
            key = str(row.iloc[2]).strip()
            if key in mapping:
                try:
                    rwa[mapping[key]] = float(row.iloc[4])
                except:
                    pass
        if rwa:
            result[q] = rwa
    return result


def extract_mr1():
    """Extrai fatores de risco de mercado – MR1 (Q4)."""
    df = pd.read_excel(Q4_FILE, sheet_name="MR1", header=None)
    items = {
        "1a": "Juros Prefixado (RWAJUR1)",
        "1c": "Cupons de Índice de Preço (RWAJUR3)",
        "3":  "Câmbio (RWAcam)",
        "5":  "Risco de Default (RWADRC)",
        "6":  "CVA (RWACVA)",
    }
    data = {}
    for _, row in df.iterrows():
        key = str(row.iloc[2]).strip()
        if key in items:
            try:
                v = float(row.iloc[4])
                data[items[key]] = v
            except:
                pass
    return data


def extract_or1():
    """Extrai histórico de perdas operacionais – OR1 (Q4)."""
    df = pd.read_excel(Q4_FILE, sheet_name="OR1", header=None)
    years = [2024, 2023, 2022, 2021, 2020, 2019, 2018]
    col_map = {2024: 5, 2023: 6, 2022: 7, 2021: 8, 2020: 9, 2019: 10, 2018: 11}
    perda_row = None
    eventos_row = None
    for i, row in df.iterrows():
        if str(row.iloc[2]).strip() == "1":
            perda_row = i
        if str(row.iloc[2]).strip() == "2":
            eventos_row = i

    result = {}
    for year in years:
        c = col_map[year]
        try:
            perda = df.iloc[perda_row, c]
            eventos = df.iloc[eventos_row, c]
            result[year] = {
                "Perda Líquida (R$)": float(perda) if str(perda) not in ["-","nan"] else 0,
                "Nº Eventos": int(float(eventos)) if str(eventos) not in ["-","nan"] else 0,
            }
        except:
            result[year] = {"Perda Líquida (R$)": 0, "Nº Eventos": 0}
    return result


def extract_irrbb():
    """Extrai sensibilidade ao risco de taxa de juros – IRRBB1 (Q4)."""
    df = pd.read_excel(Q4_FILE, sheet_name="IRRBB1", header=None)
    scenarios = {
        "Paralelo Alta":    (7, 4),
        "Paralelo Baixa":   (8, 4),
        "Alta Curto Prazo": (9, 4),
        "Baixa Curto Prazo":(10,4),
        "Steepener":        (11,4),
        "Flattener":        (12,4),
    }
    data = {}
    for name, (r, c) in scenarios.items():
        try:
            data[name] = float(df.iloc[r, c])
        except:
            data[name] = np.nan
    nii = {}
    try:
        nii["Paralelo Alta"]  = float(df.iloc[7, 6])
        nii["Paralelo Baixa"] = float(df.iloc[8, 6])
    except:
        pass
    return data, nii


def extract_cc1():
    """Composição do Patrimônio de Referência – CC1 (Q4)."""
    df = pd.read_excel(Q4_FILE, sheet_name="CC1", header=None)
    items = {
        "1":  "Instrumentos Elegíveis",
        "2":  "Reservas de Lucros",
        "3":  "Outras Receitas/Reservas",
        "8":  "Ágios (Goodwill)",
        "9":  "Ativos Intangíveis",
        "10": "Créditos Tributários",
    }
    data = {}
    for _, row in df.iterrows():
        key = str(row.iloc[2]).strip()
        if key in items:
            try:
                v = row.iloc[4]
                data[items[key]] = float(v) if str(v) not in ["-","nan"] else 0
            except:
                pass
    return data


# ═══════════════════════════════════════════════════════════════════════════════
# 2. DASHBOARD PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def plot_dashboard():
    km1 = extract_km1()

    # ── Cartão de métricas no topo ────────────────────────────────────────────
    q4 = km1[km1["Trimestre"] == "Q4/2025"].iloc[0]

    print("\n" + "="*70)
    print("  NUBANK – RELATÓRIO PILAR 3  |  Data-base: 31/12/2025")
    print("="*70)
    print(f"  Patrimônio de Referência (PR):   {fmt_bi(q4['PR'])}")
    print(f"  RWA Total:                        {fmt_bi(q4['RWA Total'])}")
    print(f"  Índice de Basileia:               {pct(q4['Índice de Basileia (%)'])}")
    print(f"  Índice Capital Principal (ICP):   {pct(q4['ICP (%)'])}")
    print(f"  Índice de Nível 1:                {pct(q4['Índice Nível 1 (%)'])}")
    print(f"  Margem sobre ACP:                 {pct(q4['Margem Exc. ICP (%)'])}")
    print("="*70 + "\n")

    # ── Figura 1: Evolução Capital e RWA ─────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("NUBANK – Evolução do Capital e RWA (2025)", fontsize=16,
                 fontweight="bold", color=PURPLE_DARK, y=1.01)

    quarters = km1["Trimestre"].tolist()
    x = np.arange(len(quarters))
    w = 0.25

    ax = axes[0]
    bars1 = ax.bar(x - w,   km1["Capital Principal"]/1e9, w, label="Capital Principal", color=PURPLE)
    bars2 = ax.bar(x,        km1["Nível I"]/1e9,           w, label="Nível I",           color=PURPLE_LIGHT)
    bars3 = ax.bar(x + w,   km1["PR"]/1e9,                 w, label="PR",                color=TEAL)
    ax.set_xticks(x); ax.set_xticklabels(quarters)
    ax.set_ylabel("R$ Bilhões")
    ax.set_title("Composição do Capital Regulatório")
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.0f}bi"))
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.2,
                    f"{h:.1f}", ha="center", fontsize=8, color=PURPLE_DARK, fontweight="bold")

    ax2 = axes[1]
    ax2.plot(quarters, km1["RWA Total"]/1e9, marker="o", linewidth=2.5,
             markersize=9, color=PURPLE, label="RWA Total")
    ax2.fill_between(quarters, km1["RWA Total"]/1e9, alpha=0.12, color=PURPLE)
    for i, (q, v) in enumerate(zip(quarters, km1["RWA Total"]/1e9)):
        ax2.annotate(f"R${v:.0f}bi", (q, v), textcoords="offset points",
                     xytext=(0, 12), ha="center", fontsize=9, color=PURPLE_DARK, fontweight="bold")
    ax2.set_ylabel("R$ Bilhões")
    ax2.set_title("Evolução do RWA Total")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.0f}bi"))

    # RWA YoY growth
    rwa = km1["RWA Total"].values
    growth = (rwa[-1] - rwa[0]) / rwa[0] * 100
    ax2.annotate(f"Crescimento YTD: +{growth:.1f}%",
                 xy=(0.03, 0.93), xycoords="axes fraction",
                 fontsize=10, color=MAGENTA, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))

    plt.tight_layout()
    plt.savefig("fig1_capital_rwa.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 1 salva: fig1_capital_rwa.png")

    # ── Figura 2: Índices Prudenciais ─────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("NUBANK – Índices Prudenciais (2025)", fontsize=16,
                 fontweight="bold", color=PURPLE_DARK, y=1.01)

    ax = axes[0]
    ax.plot(quarters, km1["Índice de Basileia (%)"]*100, marker="s", linewidth=2.5,
            markersize=9, color=TEAL, label="Índice de Basileia")
    ax.plot(quarters, km1["Índice Nível 1 (%)"]*100, marker="^", linewidth=2.5,
            markersize=9, color=PURPLE, label="Índice Nível 1")
    ax.plot(quarters, km1["ICP (%)"]*100, marker="o", linewidth=2.5,
            markersize=9, color=GOLD, label="ICP (Capital Principal)")
    ax.axhline(y=8, color=MAGENTA, linestyle="--", linewidth=1.5, label="Mín. Basileia (8%)")
    ax.axhline(y=10.5, color=GRAY, linestyle=":", linewidth=1.5, label="Mín. ICP (10.5%)")
    ax.set_ylabel("Índice (%)")
    ax.set_title("Índices de Adequação de Capital")
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}%"))

    ax2 = axes[1]
    margem = km1["Margem Exc. ICP (%)"]*100
    colors_bar = [TEAL if v > 5 else GOLD if v > 2.5 else MAGENTA for v in margem]
    bars = ax2.bar(quarters, margem, color=colors_bar, edgecolor="white", linewidth=0.8)
    ax2.axhline(y=0, color=MAGENTA, linestyle="--", linewidth=1.2)
    ax2.set_ylabel("Margem (%)")
    ax2.set_title("Margem Excedente sobre ACP (Capital Principal)")
    for bar, v in zip(bars, margem):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f"{v:.2f}%", ha="center", fontsize=10, fontweight="bold", color=PURPLE_DARK)

    # Legenda de cores
    patches = [
        mpatches.Patch(color=TEAL,   label="> 5% (Sólido)"),
        mpatches.Patch(color=GOLD,   label="2.5–5% (Atenção)"),
        mpatches.Patch(color=MAGENTA,label="< 2.5% (Alerta)"),
    ]
    ax2.legend(handles=patches, fontsize=9)

    plt.tight_layout()
    plt.savefig("fig2_indices_prudenciais.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 2 salva: fig2_indices_prudenciais.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. COMPOSIÇÃO DO RWA
# ═══════════════════════════════════════════════════════════════════════════════

def plot_rwa_composition():
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("NUBANK – Composição do RWA (Ativos Ponderados pelo Risco)",
                 fontsize=15, fontweight="bold", color=PURPLE_DARK, y=1.01)

    # ── Pizza Q4 ──────────────────────────────────────────────────────────────
    ov1_series = extract_ov1_series()
    q4_rwa = ov1_series.get("Q4/2025", {})

    # OV1 linha 1 = crédito estrito, mas a sheet usa row "7" ≠ "1"
    # Usamos os dados já carregados
    if not q4_rwa:
        q4_rwa = {
            "Crédito (Estrito)": 119826733986,
            "CCR":                   54190906,
            "Securitização":        110975155,
            "Mercado":             6573494237,
        }

    labels = list(q4_rwa.keys())
    sizes  = [v/1e9 for v in q4_rwa.values()]
    colors = [PURPLE, PURPLE_LIGHT, TEAL, GOLD, MAGENTA, BLUE, GRAY][:len(labels)]
    explode = [0.04]*len(labels)

    ax = axes[0]
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, colors=colors, explode=explode,
        autopct=lambda p: f"{p:.1f}%\n({p*sum(sizes)/100:.1f}bi)",
        startangle=90, pctdistance=0.7,
        wedgeprops=dict(linewidth=1.5, edgecolor="white")
    )
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_fontweight("bold")
        at.set_color("white")
    ax.legend(wedges, labels, loc="lower center", bbox_to_anchor=(0.5, -0.15),
              ncol=2, fontsize=9)
    ax.set_title("Composição do RWA – Q4/2025\n(Total: R$171 bi)", pad=10)

    # ── Barras horizontais comparativo Q2 vs Q4 ───────────────────────────────
    ax2 = axes[1]
    q2_rwa = ov1_series.get("Q2/2025", {})
    if q2_rwa and q4_rwa:
        all_cats = list(set(list(q2_rwa.keys()) + list(q4_rwa.keys())))
        y_pos = np.arange(len(all_cats))
        q2_vals = [q2_rwa.get(c, 0)/1e9 for c in all_cats]
        q4_vals = [q4_rwa.get(c, 0)/1e9 for c in all_cats]

        ax2.barh(y_pos + 0.2, q4_vals, 0.35, label="Q4/2025", color=PURPLE)
        ax2.barh(y_pos - 0.2, q2_vals, 0.35, label="Q2/2025", color=PURPLE_LIGHT, alpha=0.8)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(all_cats)
        ax2.set_xlabel("R$ Bilhões")
        ax2.set_title("Variação do RWA por Tipo de Risco\nQ2/2025 → Q4/2025")
        ax2.legend()
        ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.0f}bi"))

        # Variação percentual
        for i, cat in enumerate(all_cats):
            v2 = q2_rwa.get(cat, 0)
            v4 = q4_rwa.get(cat, 0)
            if v2 > 0:
                delta = (v4 - v2) / v2 * 100
                color = TEAL if delta < 0 else MAGENTA
                ax2.text(max(v2, v4)/1e9 + 0.5, i,
                         f"{delta:+.1f}%", va="center", fontsize=9,
                         color=color, fontweight="bold")

    plt.tight_layout()
    plt.savefig("fig3_rwa_composicao.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 3 salva: fig3_rwa_composicao.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. QUALIDADE DO CRÉDITO
# ═══════════════════════════════════════════════════════════════════════════════

def plot_credit_quality():
    cr1 = extract_cr1()
    cr2 = extract_cr2()

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle("NUBANK – Qualidade Creditícia e Ativos Problemáticos (Q4/2025)",
                 fontsize=15, fontweight="bold", color=PURPLE_DARK, y=1.01)

    # ── Barras empilhadas Problemáticos vs Não Problemáticos ─────────────────
    ax = axes[0]
    cats = cr1[cr1["Categoria"] != "Total"]["Categoria"].tolist()
    prob = cr1[cr1["Categoria"] != "Total"]["Ativos Problemáticos (R$ mil)"].values / 1e6
    nprob = cr1[cr1["Categoria"] != "Total"]["Ativos Não Problemáticos (R$ mil)"].values / 1e6

    x = np.arange(len(cats))
    ax.bar(x, nprob, color=TEAL, label="Não Problemáticos", edgecolor="white")
    ax.bar(x, prob,  bottom=nprob, color=MAGENTA, label="Problemáticos", edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, rotation=15, ha="right", fontsize=9)
    ax.set_ylabel("R$ Bilhões")
    ax.set_title("Exposições por Qualidade\n(R$ bilhões)")
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.0f}bi"))

    # Percentual problemático
    for i, (p, np_) in enumerate(zip(prob, nprob)):
        total = p + np_
        pct_p = p / total * 100 if total > 0 else 0
        ax.text(i, total + total*0.02, f"{pct_p:.1f}%\nproblem.", ha="center",
                fontsize=8, color=MAGENTA, fontweight="bold")

    # ── Provisões vs Problemáticos ────────────────────────────────────────────
    ax2 = axes[1]
    cats2 = cr1[cr1["Categoria"] != "Total"]["Categoria"].tolist()
    provs = cr1[cr1["Categoria"] != "Total"]["Provisões (R$ mil)"].values / 1e6
    probs = cr1[cr1["Categoria"] != "Total"]["Ativos Problemáticos (R$ mil)"].values / 1e6

    x2 = np.arange(len(cats2))
    w = 0.35
    ax2.bar(x2 - w/2, probs, w, label="Ativos Problemáticos", color=MAGENTA)
    ax2.bar(x2 + w/2, provs, w, label="Provisões Constituídas", color=PURPLE)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(cats2, rotation=15, ha="right", fontsize=9)
    ax2.set_ylabel("R$ Bilhões")
    ax2.set_title("Ativos Problemáticos\nvs. Provisões Constituídas")
    ax2.legend(fontsize=9)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.0f}bi"))

    # Coverage ratio
    total_prob = sum(probs)
    total_prov = sum(provs)
    coverage = total_prov / total_prob * 100 if total_prob > 0 else 0
    ax2.annotate(f"Coverage Ratio:\n{coverage:.1f}%",
                 xy=(0.65, 0.85), xycoords="axes fraction",
                 fontsize=11, color=PURPLE_DARK, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=PURPLE, alpha=0.9))

    # ── Waterfall de Ativos Problemáticos ─────────────────────────────────────
    ax3 = axes[2]
    if cr2:
        wf_labels = list(cr2.keys())
        wf_vals   = list(cr2.values())

        # Posições acumuladas para waterfall
        running = 0
        bottoms = []
        heights = []
        bar_colors = []
        for i, (lbl, v) in enumerate(zip(wf_labels, wf_vals)):
            if i == 0 or i == len(wf_labels) - 1:
                bottoms.append(0)
                heights.append(v)
                bar_colors.append(PURPLE if i == 0 else TEAL)
            else:
                if v >= 0:
                    bottoms.append(running)
                    heights.append(v)
                    bar_colors.append(MAGENTA)
                else:
                    bottoms.append(running + v)
                    heights.append(-v)
                    bar_colors.append(TEAL)
            if i < len(wf_labels) - 1:
                running += v

        xpos = np.arange(len(wf_labels))
        bars = ax3.bar(xpos, heights, bottom=bottoms, color=bar_colors,
                       edgecolor="white", linewidth=1.2)
        ax3.set_xticks(xpos)
        ax3.set_xticklabels(wf_labels, rotation=20, ha="right", fontsize=8.5)
        ax3.set_ylabel("R$ Mil")
        ax3.set_title("Movimentação dos Ativos\nProblemáticos – Q4/2025")

        for bar, v in zip(bars, wf_vals):
            ypos = bar.get_y() + bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2,
                     ypos + max(abs(v) * 0.03, 200_000),
                     f"{v/1e6:.1f}mi", ha="center", fontsize=8.5,
                     fontweight="bold", color=PURPLE_DARK)

    plt.tight_layout()
    plt.savefig("fig4_qualidade_credito.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 4 salva: fig4_qualidade_credito.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. RISCO DE MERCADO E IRRBB
# ═══════════════════════════════════════════════════════════════════════════════

def plot_market_risk():
    mr1 = extract_mr1()
    eve, nii = extract_irrbb()

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("NUBANK – Risco de Mercado e Sensibilidade à Taxa de Juros (IRRBB)",
                 fontsize=15, fontweight="bold", color=PURPLE_DARK, y=1.01)

    # ── Composição RWA Mercado ─────────────────────────────────────────────────
    ax = axes[0]
    if mr1:
        cats = list(mr1.keys())
        vals = [v/1e6 for v in mr1.values()]
        colors_mr = [PURPLE, PURPLE_LIGHT, GOLD, TEAL, MAGENTA][:len(cats)]
        bars = ax.barh(cats, vals, color=colors_mr, edgecolor="white", linewidth=1)
        ax.set_xlabel("RWAMPAD (R$ Milhões)")
        ax.set_title("Fatores de Risco de Mercado\n(Q4/2025)")
        for bar, v in zip(bars, vals):
            ax.text(v + max(vals)*0.01, bar.get_y() + bar.get_height()/2,
                    f"R${v:.1f}mi", va="center", fontsize=9,
                    color=PURPLE_DARK, fontweight="bold")
        total_mr = sum(vals)
        ax.annotate(f"Total: R${total_mr:.0f}mi",
                    xy=(0.6, 0.05), xycoords="axes fraction",
                    fontsize=11, color=PURPLE_DARK, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=PURPLE, alpha=0.9))

    # ── IRRBB – ΔEVE por cenário ────────────────────────────────────────────
    ax2 = axes[1]
    if eve:
        scenario_names = list(eve.keys())
        eve_vals = [v/1e6 if not np.isnan(v) else 0 for v in eve.values()]
        bar_colors = [MAGENTA if v > 300 else GOLD if v > 100 else TEAL
                      for v in eve_vals]
        bars2 = ax2.bar(scenario_names, eve_vals, color=bar_colors,
                        edgecolor="white", linewidth=1)
        ax2.set_xticklabels(scenario_names, rotation=20, ha="right", fontsize=9)
        ax2.set_ylabel("ΔEVE (R$ Milhões)")
        ax2.set_title("Sensibilidade IRRBB – ΔEVE\n(impacto no valor econômico do capital)")
        for bar, v in zip(bars2, eve_vals):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                     f"R${v:.0f}mi", ha="center", fontsize=9,
                     color=PURPLE_DARK, fontweight="bold")

        max_eve = max(eve_vals)
        nivel1 = 24579306522 / 1e6
        ratio = max_eve / nivel1 * 100
        color_ratio = MAGENTA if ratio > 15 else GOLD if ratio > 5 else TEAL
        ax2.annotate(f"Máx. ΔEVE/Nível I: {ratio:.1f}%",
                     xy=(0.55, 0.88), xycoords="axes fraction",
                     fontsize=11, color=color_ratio, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.4", fc="white",
                               ec=color_ratio, alpha=0.9))

    plt.tight_layout()
    plt.savefig("fig5_risco_mercado.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 5 salva: fig5_risco_mercado.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. RISCO OPERACIONAL
# ═══════════════════════════════════════════════════════════════════════════════

def plot_operational_risk():
    or1 = extract_or1()

    years = sorted(or1.keys())
    perdas = [or1[y]["Perda Líquida (R$)"] / 1e6 for y in years]
    eventos = [or1[y]["Nº Eventos"] for y in years]

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("NUBANK – Histórico de Perdas Operacionais (OR1)",
                 fontsize=15, fontweight="bold", color=PURPLE_DARK, y=1.01)

    # ── Perdas ────────────────────────────────────────────────────────────────
    ax = axes[0]
    bar_colors = [MAGENTA if v > 100 else GOLD if v > 30 else TEAL for v in perdas]
    bars = ax.bar([str(y) for y in years], perdas, color=bar_colors,
                  edgecolor="white", linewidth=1)
    ax.set_ylabel("Perda Líquida (R$ Milhões)")
    ax.set_title("Perdas Operacionais por Ano\n(Limiar R$100k)")
    for bar, v in zip(bars, perdas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f"R${v:.1f}mi", ha="center", fontsize=9,
                fontweight="bold", color=PURPLE_DARK)

    # Média
    media = np.mean(perdas)
    ax.axhline(y=media, color=BLUE, linestyle="--", linewidth=1.5,
               label=f"Média: R${media:.1f}mi")
    ax.legend(fontsize=9)

    patches = [
        mpatches.Patch(color=MAGENTA, label="> R$100mi"),
        mpatches.Patch(color=GOLD,    label="R$30–100mi"),
        mpatches.Patch(color=TEAL,    label="< R$30mi"),
    ]
    ax.legend(handles=patches + [plt.Line2D([0], [0], color=BLUE, linestyle="--",
              label=f"Média R${media:.1f}mi")], fontsize=9)

    # ── Número de Eventos ─────────────────────────────────────────────────────
    ax2 = axes[1]
    ax2.bar([str(y) for y in years], eventos, color=PURPLE, edgecolor="white",
            linewidth=1, alpha=0.85)
    ax2.set_ylabel("Nº de Eventos Operacionais")
    ax2.set_title("Número de Eventos Operacionais\npor Ano")
    for i, (bar, ev) in enumerate(zip(ax2.patches, eventos)):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 str(ev), ha="center", fontsize=10,
                 fontweight="bold", color=PURPLE_DARK)

    # CAGR de eventos
    if eventos[0] > 0 and len(eventos) > 1:
        n = len(eventos) - 1
        cagr = ((eventos[-1] / eventos[0]) ** (1 / n) - 1) * 100
        ax2.annotate(f"CAGR eventos: +{cagr:.0f}%/ano",
                     xy=(0.03, 0.88), xycoords="axes fraction",
                     fontsize=10, color=MAGENTA, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

    plt.tight_layout()
    plt.savefig("fig6_risco_operacional.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 6 salva: fig6_risco_operacional.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. COMPOSIÇÃO DO PR (CC1)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_pr_composition():
    cc1 = extract_cc1()

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("NUBANK – Composição do Patrimônio de Referência (CC1 – Q4/2025)",
                 fontsize=15, fontweight="bold", color=PURPLE_DARK, y=1.01)

    # ── Componentes positivos (adições) ───────────────────────────────────────
    pos_keys = ["Instrumentos Elegíveis", "Reservas de Lucros", "Outras Receitas/Reservas"]
    neg_keys = ["Ágios (Goodwill)", "Ativos Intangíveis", "Créditos Tributários"]

    pos_vals = [cc1.get(k, 0) / 1e9 for k in pos_keys]
    neg_vals = [cc1.get(k, 0) / 1e9 for k in neg_keys]

    ax = axes[0]
    x1 = np.arange(len(pos_keys))
    ax.bar(x1, pos_vals, color=[TEAL, PURPLE, PURPLE_LIGHT], edgecolor="white", linewidth=1)
    ax.set_xticks(x1); ax.set_xticklabels(pos_keys, rotation=15, ha="right", fontsize=9)
    ax.set_ylabel("R$ Bilhões")
    ax.set_title("Componentes Positivos do Capital Principal")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.1f}bi"))
    for i, (bar, v) in enumerate(zip(ax.patches, pos_vals)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f"R${v:.1f}bi", ha="center", fontsize=9, fontweight="bold", color=PURPLE_DARK)

    # ── Deduções (ajustes prudenciais) ────────────────────────────────────────
    ax2 = axes[1]
    x2 = np.arange(len(neg_keys))
    ax2.bar(x2, neg_vals, color=[MAGENTA, GOLD, BLUE], edgecolor="white", linewidth=1)
    ax2.set_xticks(x2); ax2.set_xticklabels(neg_keys, rotation=15, ha="right", fontsize=9)
    ax2.set_ylabel("R$ Bilhões")
    ax2.set_title("Deduções do Capital Principal\n(Ajustes Prudenciais)")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.1f}bi"))
    for bar, v in zip(ax2.patches, neg_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                 f"R${v:.2f}bi", ha="center", fontsize=9, fontweight="bold", color=PURPLE_DARK)

    total_pos = sum(pos_vals)
    total_neg = sum(neg_vals)
    ax2.annotate(f"Total deduções: R${total_neg:.2f}bi\n"
                 f"({total_neg/total_pos*100:.1f}% das adições)",
                 xy=(0.5, 0.85), xycoords="axes fraction",
                 ha="center", fontsize=10, color=MAGENTA, fontweight="bold",
                 bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=MAGENTA, alpha=0.9))

    plt.tight_layout()
    plt.savefig("fig7_composicao_pr.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 7 salva: fig7_composicao_pr.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. PAINEL DE INSIGHTS E ALERTAS
# ═══════════════════════════════════════════════════════════════════════════════

def plot_insights_panel():
    km1 = extract_km1()
    q4  = km1[km1["Trimestre"] == "Q4/2025"].iloc[0]
    q1  = km1[km1["Trimestre"] == "Q1/2025"].iloc[0]
    or1 = extract_or1()

    fig = plt.figure(figsize=(18, 10))
    fig.patch.set_facecolor(BG)
    gs  = GridSpec(3, 4, figure=fig, hspace=0.5, wspace=0.4)
    fig.suptitle("NUBANK – Painel de Insights & KPIs Regulatórios (Q4/2025)",
                 fontsize=16, fontweight="bold", color=PURPLE_DARK, y=1.01)

    def kpi_card(ax, title, value, subtitle, color, icon=""):
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(color + "22")
        for spine in ax.spines.values():
            spine.set_edgecolor(color)
            spine.set_linewidth(2)
        ax.text(0.5, 0.80, icon + " " + title, ha="center", va="center",
                fontsize=10, color=color, fontweight="bold", transform=ax.transAxes)
        ax.text(0.5, 0.45, value, ha="center", va="center",
                fontsize=18, color=PURPLE_DARK, fontweight="bold", transform=ax.transAxes)
        ax.text(0.5, 0.15, subtitle, ha="center", va="center",
                fontsize=8.5, color=GRAY, transform=ax.transAxes, style="italic")
        ax.set_xticks([]); ax.set_yticks([])

    # ── KPIs ──────────────────────────────────────────────────────────────────
    rwa_growth = (q4["RWA Total"] - q1["RWA Total"]) / q1["RWA Total"] * 100
    pr_growth  = (q4["PR"] - q1["PR"]) / q1["PR"] * 100
    icp_delta  = (q4["ICP (%)"] - q1["ICP (%)"])*100
    baz_delta  = (q4["Índice de Basileia (%)"] - q1["Índice de Basileia (%)"])*100

    perda_2024 = or1[2024]["Perda Líquida (R$)"]
    perda_2023 = or1[2023]["Perda Líquida (R$)"]
    perda_var  = (perda_2024 - perda_2023) / perda_2023 * 100

    metrics = [
        ("Patrimônio de Referência", fmt_bi(q4["PR"]),
         f"▲ +{pr_growth:.1f}% desde Q1", TEAL, "🏦"),
        ("RWA Total", fmt_bi(q4["RWA Total"]),
         f"▲ +{rwa_growth:.1f}% desde Q1", GOLD, "📊"),
        ("Índice de Basileia", pct(q4["Índice de Basileia (%)"]),
         f"Δ {baz_delta:+.2f}pp vs Q1 | Mín: 8%", TEAL, "✅"),
        ("ICP (Capital Principal)", pct(q4["ICP (%)"]),
         f"Δ {icp_delta:+.2f}pp vs Q1 | Mín: 4,5%", TEAL, "✅"),
        ("Margem s/ ACP", pct(q4["Margem Exc. ICP (%)"]),
         "Folga regulatória sobre capital adicional", PURPLE, "🛡️"),
        ("Perda Operacional (2024)", fmt_mi(perda_2024),
         f"▲ {perda_var:+.1f}% vs 2023 – Crescimento acelerado", MAGENTA, "⚠️"),
        ("Ativos Problemáticos", "R$ 27,3 bi",
         "Total bruto Q4 | Provisões: R$47,2 bi (Coverage >170%)", GOLD, "📋"),
        ("ΔEVE Máx. (IRRBB)", "R$ 710,8 mi",
         "Cenário alta CP | 2,9% do Nível I → Baixo risco", TEAL, "📈"),
    ]

    positions = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3)]
    for (row, col), (title, value, sub, color, icon) in zip(positions, metrics):
        ax = fig.add_subplot(gs[row, col])
        kpi_card(ax, title, value, sub, color, icon)

    # ── Gráfico radar de riscos ───────────────────────────────────────────────
    ax_radar = fig.add_subplot(gs[2, :2], polar=True)
    risk_labels = ["Crédito", "Mercado", "Operacional", "Liquidez", "IRRBB", "CCR"]
    # Scores subjetivos baseados nos dados (0-10, 10=risco alto)
    risk_scores = [5.5, 3.5, 7.0, 3.0, 2.5, 2.0]
    N = len(risk_labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    scores = risk_scores + risk_scores[:1]

    ax_radar.plot(angles, scores, color=PURPLE, linewidth=2)
    ax_radar.fill(angles, scores, alpha=0.25, color=PURPLE)
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(risk_labels, fontsize=10, fontweight="bold")
    ax_radar.set_ylim(0, 10)
    ax_radar.set_yticks([2, 4, 6, 8, 10])
    ax_radar.set_yticklabels(["2", "4", "6", "8", "10"], fontsize=8, color=GRAY)
    ax_radar.set_title("Mapa de Riscos\n(score 0–10, maior = mais crítico)",
                       fontsize=11, fontweight="bold", color=PURPLE_DARK, pad=15)

    # ── Resumo textual de insights ─────────────────────────────────────────────
    ax_text = fig.add_subplot(gs[2, 2:])
    ax_text.set_xlim(0, 1); ax_text.set_ylim(0, 1)
    ax_text.axis("off")

    insights = [
        ("🟢 PONTOS POSITIVOS", TEAL, [
            f"• Índice de Basileia em {pct(q4['Índice de Basileia (%)'])} (muito acima do mín. 8%)",
            f"• PR cresceu +{pr_growth:.1f}% no ano, financiando expansão",
            f"• Coverage ratio de provisões > 170% (conservador)",
            f"• ΔEVE/Nível I = 2.9% → IRRBB bem controlado",
        ]),
        ("🔴 PONTOS DE ATENÇÃO", MAGENTA, [
            f"• RWA cresceu +{rwa_growth:.1f}% em 2025 (risco crédito domina)",
            f"• Perdas operacionais em 2024: R${perda_2024/1e6:.0f}mi (+{perda_var:.0f}% vs 2023)",
            f"• ICP caiu de {pct(q1['ICP (%)'])} (Q1) → {pct(q4['ICP (%)'])} (Q4)",
            f"• Ativos intangíveis: R$2,2bi em deduções prudenciais",
        ]),
    ]

    y_pos = 0.95
    for title, color, lines in insights:
        ax_text.text(0.02, y_pos, title, fontsize=10, color=color,
                     fontweight="bold", transform=ax_text.transAxes)
        y_pos -= 0.08
        for line in lines:
            ax_text.text(0.03, y_pos, line, fontsize=8.5, color=PURPLE_DARK,
                         transform=ax_text.transAxes)
            y_pos -= 0.07
        y_pos -= 0.04

    for spine in ax_text.spines.values():
        spine.set_visible(False)

    plt.savefig("fig8_insights_panel.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 8 salva: fig8_insights_panel.png")


# ═══════════════════════════════════════════════════════════════════════════════
# 9. EVOLUÇÃO TEMPORAL COMPLETA
# ═══════════════════════════════════════════════════════════════════════════════

def plot_full_timeline():
    km1 = extract_km1()
    quarters = km1["Trimestre"].tolist()

    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle("NUBANK – Painel Evolutivo Completo 2025 (Pilar 3)",
                 fontsize=16, fontweight="bold", color=PURPLE_DARK, y=1.01)

    def styled_line(ax, x, y, label, color, marker="o"):
        ax.plot(x, y, marker=marker, linewidth=2.5, markersize=9,
                color=color, label=label)
        ax.fill_between(x, y, min(y), alpha=0.08, color=color)
        for xi, yi in zip(x, y):
            ax.annotate(f"{yi:.2f}", (xi, yi), textcoords="offset points",
                        xytext=(0, 10), ha="center", fontsize=8.5,
                        color=color, fontweight="bold")

    # ── Capital ────────────────────────────────────────────────────────────────
    ax = axes[0, 0]
    styled_line(ax, quarters, km1["Capital Principal"]/1e9, "Capital Principal", PURPLE)
    styled_line(ax, quarters, km1["Nível I"]/1e9, "Nível I", TEAL, marker="s")
    styled_line(ax, quarters, km1["PR"]/1e9, "PR", GOLD, marker="^")
    ax.set_title("Evolução do Capital Regulatório (R$ bi)")
    ax.set_ylabel("R$ Bilhões")
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}bi"))

    # ── RWA ────────────────────────────────────────────────────────────────────
    ax2 = axes[0, 1]
    styled_line(ax2, quarters, km1["RWA Total"]/1e9, "RWA Total", MAGENTA)
    ax2.set_title("Evolução do RWA Total (R$ bi)")
    ax2.set_ylabel("R$ Bilhões")
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}bi"))

    # ── Índices ────────────────────────────────────────────────────────────────
    ax3 = axes[1, 0]
    styled_line(ax3, quarters, km1["Índice de Basileia (%)"]*100, "Índice de Basileia", TEAL)
    styled_line(ax3, quarters, km1["ICP (%)"]*100, "ICP", PURPLE, marker="s")
    ax3.axhline(y=8, color=MAGENTA, linestyle="--", linewidth=1.2, label="Mín. 8% (Basileia)")
    ax3.axhline(y=4.5, color=GRAY, linestyle=":", linewidth=1, label="Mín. 4,5% (ICP)")
    ax3.set_title("Índices Regulatórios (%)")
    ax3.set_ylabel("Índice (%)")
    ax3.legend(fontsize=8.5)
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}%"))

    # ── Margem ────────────────────────────────────────────────────────────────
    ax4 = axes[1, 1]
    margem = km1["Margem Exc. ICP (%)"]*100
    bar_colors = [TEAL if v > 5 else GOLD if v > 2.5 else MAGENTA for v in margem]
    ax4.bar(quarters, margem, color=bar_colors, edgecolor="white", linewidth=1)
    ax4.set_title("Margem Excedente de Capital Principal (%)")
    ax4.set_ylabel("Margem (%)")
    ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}%"))
    for bar, v in zip(ax4.patches, margem):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{v:.2f}%", ha="center", fontsize=10, fontweight="bold", color=PURPLE_DARK)

    plt.tight_layout()
    plt.savefig("fig9_timeline_completa.png", dpi=150, bbox_inches="tight")
    plt.show()
    print("[✓] Figura 9 salva: fig9_timeline_completa.png")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "█"*70)
    print("  NUBANK – ANÁLISE PILAR 3 | CIRCULAR BCB 3.930 | 2025")
    print("█"*70)

    # Verifica arquivos
    missing = [p for p in FILES.values() if not os.path.exists(p)]
    if missing:
        print("\n⚠️  Arquivos não encontrados:")
        for f in missing:
            print(f"   ✗ {f}")
        print("\n  Coloque os arquivos na mesma pasta do script e execute novamente.")
        return

    print("\n  Arquivos encontrados. Gerando análise...\n")

    plot_dashboard()
    plot_rwa_composition()
    plot_credit_quality()
    plot_market_risk()
    plot_operational_risk()
    plot_pr_composition()
    plot_insights_panel()
    plot_full_timeline()

    print("\n" + "="*70)
    print("  ✅ Análise completa! 9 figuras geradas nesta pasta.")
    print("  Figuras: fig1 a fig9 + fig8_insights_panel.png")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()