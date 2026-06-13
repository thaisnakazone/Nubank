# 1. Importar bibliotecas
import sqlite3
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback_context
import os, webbrowser

# 2. Conectar ao banco e carregar dados
BASE_DIR = Path(__file__).resolve().parent   # pasta reports
ROOT_DIR = BASE_DIR.parent                   # sobe para Nubank/
db_path = ROOT_DIR / "data" / "nubank.db"    # caminho correto para o banco

def run_query(sql):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

# --- Preparar dados base ---
df_long = run_query("SELECT codigo, descricao, periodo, valor FROM historico_capital")
df_long["periodo"] = pd.to_datetime(df_long["periodo"], errors="coerce")
anos_disponiveis = sorted(df_long["periodo"].dropna().dt.year.unique())

# --- Criar app ---
app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f9f9f9", "padding": "20px"},
    children=[
        # Banner
        html.Div(
            children=html.H1(
                "Dashboard – Indicadores de Capital Nubank",
                style={
                    "textAlign": "center",
                    "color": "white",
                    "fontWeight": "bold",
                    "fontSize": "40px",
                    "margin": "0"
                }
            ),
            style={"backgroundColor": "#8A05BE", "padding": "20px"}
        ),
        
        # Linha com seleção de ano, botão evolução e cards
        html.Div([
            dcc.Dropdown(
                id="ano-dropdown",
                options=[{"label": str(ano), "value": ano} for ano in anos_disponiveis],
                value=2025,
                clearable=False,
                style={
                    "width": "100px",
                    "backgroundColor": "#8A05BE",
                    "color": "#8A05BE",
                    "fontWeight": "900",
                    "borderRadius": "8px",
                    "padding": "5px",
                    "marginLeft": "10px",
                    "marginRight": "25px"
                }
            ),
            html.Button("2021–2025", id="btn-todos", n_clicks=0,
                        style={
                            "padding": "12px 20px",
                            "marginRight": "40px",
                            "backgroundColor": "#FFA500",
                            "color": "white",
                            "borderRadius": "8px",
                            "border": "none",
                            "cursor": "pointer",
                            "fontWeight": "bold",
                            "fontSize": "16px"
                        }),
            html.Div(id="cards", style={"display": "flex", "gap": "20px", "marginTop": "40px","marginBottom": "30px", "marginLeft": "50px"})
        ], style={"display": "flex", "alignItems": "center", "marginBottom": "30px"}),

        # Gráficos
        html.Div([
            dcc.Graph(id="grafico-capital", style={"display": "inline-block", "width": "49%"}),
            dcc.Graph(id="grafico-comp", style={"display": "inline-block", "width": "49%"})
        ]),
        html.Div([
            dcc.Graph(id="grafico-indices", style={"display": "inline-block", "width": "49%"}),
            dcc.Graph(id="grafico-margin", style={"display": "inline-block", "width": "49%"})
        ])
    ]
)

@app.callback(
    [Output("grafico-capital", "figure"),
     Output("grafico-comp", "figure"),
     Output("grafico-indices", "figure"),
     Output("grafico-margin", "figure"),
     Output("cards", "children")],
    [Input("ano-dropdown", "value"),
     Input("btn-todos", "n_clicks")]
)
def atualizar_graficos(ano, n_todos):
    ctx = callback_context
    todos = False
    if ctx.triggered and ctx.triggered[0]["prop_id"].split(".")[0] == "btn-todos":
        todos = True

    # --- Caso especial: 2021 ---
    if ano == 2021 and not todos:
        titulo_extra = "2021"
        df_capital = df_long[(df_long["descricao"] == "Capital Principal") & (df_long["periodo"].dt.year == 2021)] \
            .groupby("periodo", as_index=False)["valor"].last()

        fig_capital = px.line(df_capital, x="periodo", y="valor", markers=True,
                              title="Evolução do Capital Principal (2021)",
                              color_discrete_sequence=["#8A05BE"])

        # Apenas um card
        cards = []
        if not df_capital.empty:
            valor_capital = df_capital["valor"].iloc[-1] / 1e9
            cards.append(html.Div([
                html.H3("Capital Principal", style={"color": "#8A05BE", "margin": "0"}),
                html.H1(f"{valor_capital:.0f} B", style={"fontSize": "32px", "fontWeight": "bold", "margin": "0"})
            ], style={"backgroundColor": "white", "padding": "15px", "borderRadius": "10px",
                      "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "textAlign": "center", "width": "200px"}))

        return fig_capital, go.Figure(), go.Figure(), go.Figure(), html.Div(cards, style={"display": "flex", "justifyContent": "center"})

    # --- Lógica normal para demais anos ou evolução ---
    if todos:
        titulo_extra = "2021–2025"
        df_capital = df_long[df_long["descricao"] == "Capital Principal"].groupby("periodo", as_index=False)["valor"].last()
        df_rwa = df_long[df_long["descricao"] == "RWA total"].groupby("periodo", as_index=False)["valor"].last()
        df_indices = df_long[df_long["descricao"].isin(["Índice de Capital Principal (ICP)", "Índice de Basileia"])] \
            .groupby(["descricao","periodo"], as_index=False)["valor"].last()
        df_margin = df_long[df_long["descricao"] == "Margem excedente de Capital Principal (%)"].groupby("periodo", as_index=False)["valor"].last()
    else:
        titulo_extra = str(ano)
        df_capital = df_long[(df_long["descricao"] == "Capital Principal") & (df_long["periodo"].dt.year == ano)] \
            .groupby("periodo", as_index=False)["valor"].last()
        df_rwa = df_long[(df_long["descricao"] == "RWA total") & (df_long["periodo"].dt.year == ano)] \
            .groupby("periodo", as_index=False)["valor"].last()
        df_indices = df_long[(df_long["descricao"].isin(["Índice de Capital Principal (ICP)", "Índice de Basileia"])) 
                             & (df_long["periodo"].dt.year == ano)] \
            .groupby(["descricao","periodo"], as_index=False)["valor"].last()
        df_margin = df_long[(df_long["descricao"] == "Margem excedente de Capital Principal (%)") 
                            & (df_long["periodo"].dt.year == ano)] \
            .groupby("periodo", as_index=False)["valor"].last()

    # Gráficos normais
    fig_capital = px.line(df_capital, x="periodo", y="valor", markers=True,
                          title=f"Evolução do Capital Principal ({titulo_extra})",
                          color_discrete_sequence=["#8A05BE"])

    fig_comp = go.Figure()
    if not df_capital.empty:
        fig_comp.add_trace(go.Scatter(x=df_capital["periodo"], y=df_capital["valor"],
                                      mode="lines+markers", name="Capital Principal", line=dict(color="#8A05BE")))
    if not df_rwa.empty:
        fig_comp.add_trace(go.Scatter(x=df_rwa["periodo"], y=df_rwa["valor"],
                                      mode="lines+markers", name="RWA Total", line=dict(color="#FF6F61")))
    fig_comp.update_layout(title=f"Capital Principal vs RWA Total ({titulo_extra})")

    fig_indices = go.Figure()
    if not df_indices.empty:
        fig_indices = px.line(df_indices, x="periodo", y="valor", color="descricao", markers=True,
                              title=f"Índice de Capital Principal vs Índice de Basileia ({titulo_extra})",
                              color_discrete_map={"Índice de Capital Principal (ICP)": "#8A05BE",
                                                  "Índice de Basileia": "#FFD700"})
        fig_indices.update_yaxes(tickformat=".0%")

    fig_margin = px.line(df_margin, x="periodo", y="valor", markers=True,
                         title=f"Margem Excedente de Capital Principal ({titulo_extra})",
                         color_discrete_sequence=["#32CD32"]) if not df_margin.empty else go.Figure()
    fig_margin.update_yaxes(tickformat=".0%")

    # Cards normais (3)
    cards = []
    if not df_capital.empty:
        valor_capital = df_capital["valor"].iloc[-1] / 1e9
        cards.append(html.Div([
            html.H3("Capital Principal", style={"color": "#8A05BE", "margin": "0"}),
            html.H1(f"{valor_capital:.0f} B", style={"fontSize": "32px", "fontWeight": "bold", "margin": "0"})
        ], style={"backgroundColor": "white", "padding": "15px", "borderRadius": "10px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "textAlign": "center", "width": "200px"}))

    if not df_rwa.empty:
        valor_rwa = df_rwa["valor"].iloc[-1] / 1e9
        cards.append(html.Div([
            html.H3("RWA Total", style={"color": "#FF6F61", "margin": "0"}),
            html.H1(f"{valor_rwa:.0f} B", style={"fontSize": "32px", "fontWeight": "bold", "margin": "0"})
        ], style={"backgroundColor": "white", "padding": "15px", "borderRadius": "10px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "textAlign": "center", "width": "200px"}))

    if not df_indices.empty:
        ultimo_periodo = df_indices["periodo"].max()
        valor_bas = df_indices[(df_indices["descricao"]=="Índice de Basileia") &
                               (df_indices["periodo"]==ultimo_periodo)]["valor"].values[0]
        cards.append(html.Div([
            html.H3("Índice de Basileia", style={"color": "#FFD700", "margin": "0"}),
            html.H1(f"{valor_bas:.1f}%", style={"fontSize": "32px", "fontWeight": "bold", "margin": "0"})
        ], style={"backgroundColor": "white", "padding": "15px", "borderRadius": "10px",
                  "boxShadow": "0 4px 8px rgba(0,0,0,0.1)", "textAlign": "center", "width": "200px"}))

    return fig_capital, fig_comp, fig_indices, fig_margin, cards

# Rodar no navegador
if __name__ == "__main__":
    port = 8050  # porta diferente da de reclamações
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        webbrowser.open(f"http://127.0.0.1:{port}")
    app.run(debug=True, use_reloader=True, port=port)