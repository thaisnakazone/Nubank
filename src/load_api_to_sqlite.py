import os
import pandas as pd
import sqlite3

def load_selic_anual():
    # Caminho robusto baseado na localização do arquivo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "..", "data", "nubank.db")
    raw_path = os.path.join(BASE_DIR, "..", "data", "raw", "bcdata.sgs.4390.csv")

    # Garantir que a pasta data existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Ler CSV da Selic acumulada no mês (SGS 4390)
    df_selic_mensal = pd.read_csv(raw_path, sep=";", decimal=",")
    df_selic_mensal["data"] = pd.to_datetime(df_selic_mensal["data"], dayfirst=True)
    df_selic_mensal["ano"] = df_selic_mensal["data"].dt.year

    # Filtrar apenas 2021 a 2025
    df_selic_mensal = df_selic_mensal[df_selic_mensal["ano"].between(2021, 2025)]

    # Converter % mensal em fator e compor (juros compostos)
    df_selic_mensal["fator"] = 1 + (df_selic_mensal["valor"] / 100)
    selic_acumulada_anual = df_selic_mensal.groupby("ano")["fator"].prod() - 1

    # Transformar em DataFrame e converter para %
    selic_acumulada_anual = selic_acumulada_anual.reset_index()
    selic_acumulada_anual.rename(columns={"fator":"selic_acumulada"}, inplace=True)
    selic_acumulada_anual["selic_acumulada"] *= 100

    # Salvar no SQLite
    conn = sqlite3.connect(db_path)
    selic_acumulada_anual.to_sql("selic_anual", conn, if_exists="replace", index=False)
    conn.close()

    print("Tabela 'selic_anual' atualizada com sucesso!")
    print(selic_acumulada_anual)


if __name__ == "__main__":
    load_selic_anual()