import os
import pandas as pd
import sqlite3

def parse_excel_matrix(path, sheet="KM1"):
    df_raw = pd.read_excel(path, sheet_name=sheet, header=None)
    letters = df_raw.iloc[5, 4:].tolist()
    dates   = df_raw.iloc[6, 4:].tolist()
    periodos = [f"{l}_{d}" for l, d in zip(letters, dates)]
    df_data = df_raw.iloc[8:, [2,3] + list(range(4, 4+len(periodos)))]
    df_data.columns = ["codigo", "descricao"] + periodos
    df_long = df_data.melt(id_vars=["codigo","descricao"], var_name="periodo", value_name="valor")
    df_long = df_long.dropna(subset=["descricao","valor"])
    df_long["periodo"] = df_long["periodo"].str.extract(r'(\d{4}-\d{2}-\d{2})')
    df_long["valor"] = pd.to_numeric(df_long["valor"], errors="coerce")
    return df_long

def load_xlsx_to_sqlite():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "..", "data", "nubank.db")
    raw_root = os.path.join(BASE_DIR, "..", "data", "raw")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # --- Tratamento especial para 2021 (CC1) ---
    map_periodo_2021 = {
        "anexo-pilar3-circular-3930-q2-2021.xlsx": "2021-06-30",
        "anexo-pilar3-circular-3930-q4-2021.xlsx": "2021-12-31"
    }
    root_2021 = os.path.join(raw_root, "2021")
    if os.path.exists(root_2021):
        for file in os.listdir(root_2021):
            if file.endswith(".xlsx") and not file.startswith("~$"):
                prefix = file.replace(".xlsx", "")
                xls = pd.ExcelFile(os.path.join(root_2021, file))
                if "CC1" in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name="CC1", skiprows=3)
                    df = df.iloc[:, :3]
                    df.columns = ["codigo", "descricao", "valor"]
                    df["periodo"] = map_periodo_2021.get(file, None)
                    table_name = f"{prefix}_CC1".replace(" ", "_")
                    df.to_sql(table_name, conn, if_exists="replace", index=False)
                    print(f"Tabela {table_name} criada com {len(df)} registros.")

    # --- Tratamento especial para Q1 2022 (KM1) ---
    path_q1_2022 = os.path.join(raw_root, "2022", "anexo-pilar3-circular-3930-q1-2022.xlsx")
    if os.path.exists(path_q1_2022):
        df_raw = pd.read_excel(path_q1_2022, sheet_name="KM1", header=None)
        periodos = list(df_raw.iloc[2, 2:].dropna().astype(str))
        df_data = df_raw.iloc[4:, 0:2+len(periodos)].copy()
        df_data.columns = ["codigo", "descricao"] + periodos
        df_long = pd.melt(df_data, id_vars=["codigo","descricao"], value_vars=periodos,
                          var_name="periodo", value_name="valor")
        df_long = df_long.dropna(subset=["descricao","valor"])
        df_long["valor"] = pd.to_numeric(df_long["valor"], errors="coerce")
        df_long["periodo"] = "2022-03-31"
        df_long.to_sql("anexo_pilar3_q1_2022_KM1", conn, if_exists="replace", index=False)
        print(f"Tabela anexo_pilar3_q1_2022_KM1 criada com {len(df_long)} registros.")

    # --- Demais arquivos (2022–2025 KM1) ---
    for root, dirs, files in os.walk(raw_root):
        for file in files:
            if file.endswith(".xlsx") and not file.startswith("~$"):
                if "2022" in root and "q1" in file.lower():
                    continue  # pula Q1 2022
                if "2021" in root:
                    continue  # pula 2021 (já tratado)
                path = os.path.join(root, file)
                df_long = parse_excel_matrix(path, "KM1")
                table_name = f"{file.replace('.xlsx','')}_KM1".replace(" ", "_")
                df_long.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"Tabela {table_name} criada com {len(df_long)} registros.")

    # --- Consolidar todas em historico_capital ---
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = [t[0] for t in cursor.fetchall()]
    tabelas_relevantes = [t for t in tabelas if ("CC1" in t or "KM1" in t)]

    if not tabelas_relevantes:
        print("Nenhuma tabela relevante encontrada, nada para consolidar.")
        conn.close()
        return []

    dfs = []
    for t in tabelas_relevantes:
        df = pd.read_sql_query(f"SELECT codigo, descricao, periodo, valor FROM '{t}'", conn)
        df["origem_tabela"] = t
        dfs.append(df)

    df_hist = pd.concat(dfs, ignore_index=True)
    df_hist.to_sql("historico_capital", conn, if_exists="replace", index=False)
    print(f"Tabela 'historico_capital' criada com {len(df_hist)} registros.")

    conn.close()
    return tabelas_relevantes

if __name__ == "__main__":
    tabelas = load_xlsx_to_sqlite()
    print("Tabelas carregadas:", tabelas)