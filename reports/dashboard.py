from dash import Dash, dcc, html, Input, Output
from pathlib import Path
import os
import plotly.express as px
import sqlite3
import pandas as pd
import webbrowser

# Conectar ao banco e carregar dados
BASE_DIR = Path(__file__).resolve().parent  # Pega a pasta do arquivo atual (reports)
ROOT_DIR = BASE_DIR.parent  # Sobe um nível (vai para Nubank)
db_path = ROOT_DIR / "data" / "nubank.db"   # Monta o caminho correto para o banco

conn = sqlite3.connect(db_path)
df_insights = pd.read_sql("SELECT * FROM reclamacoes_com_insights", conn)
conn.close()

# Criar app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f9f9f9", "padding": "20px"},
    children=[
        html.Div(
            children=html.H1(
                "Dashboard – Reclamações Nubank",
                style={
                    "textAlign": "center",
                    "color": "white",
                    "fontWeight": "bold",
                    "fontSize": "40px",
                    "margin": "0"
                }
            ),
            style={
                "backgroundColor": "#8A05BE",
                "padding": "20px"
            }
        ),

        dcc.Dropdown(
            id="categoria-dropdown",
            options=[{"label": cat, "value": cat} for cat in df_insights["Categoria_Primaria"].unique()],
            value=df_insights["Categoria_Primaria"].unique()[0],
            clearable=False,
            style={
                "width": "50%",
                "margin": "20px auto",
                "border": "2px solid #8A05BE",
                "borderRadius": "8px",
                "padding": "10px",
                "backgroundColor": "#f0e6f9",
                "color": "#8A05BE",
                "fontWeight": "bold",
                "fontSize": "16px"
            }
        ),

        html.Div([
            dcc.Graph(id="grafico-barras", style={"display": "inline-block", "width": "49%"}),
            dcc.Graph(id="grafico-pizza", style={"display": "inline-block", "width": "49%"})
        ])
    ]
)

# Callback
@app.callback(
    [Output("grafico-barras", "figure"),
     Output("grafico-pizza", "figure")],
    Input("categoria-dropdown", "value")
)
def update_graphs(categoria):
    df_filtrado = df_insights[df_insights["Categoria_Primaria"] == categoria]

    fig_bar = px.bar(
        df_filtrado,
        x="Severidade_Estimada",
        title=f"Severidade - {categoria}",
        color_discrete_sequence=["#8A05BE"]
    )

    fig_pie = px.pie(
        df_filtrado,
        names="Severidade_Estimada",
        title=f"Distribuição de Severidade - {categoria}",
        color_discrete_sequence=["#8A05BE", "#FF6F61", "#FFD700", "#00BFFF", "#32CD32"]
    )

    return fig_bar, fig_pie

# Rodar no navegador
if __name__ == "__main__":
    port = 8051
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        webbrowser.open(f"http://127.0.0.1:{port}")
    app.run(debug=True, use_reloader=True, port=port)