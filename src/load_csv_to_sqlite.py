import os
import pandas as pd
import sqlite3

def load_csvs_to_sqlite(db_path="../data/nubank.db", processed_path="../data/processed"):
    # Garantir que a pasta data existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Criar/abrir banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ler CSVs e salvar como tabelas
    for file in os.listdir(processed_path):
        if file.endswith(".csv"):
            table_name = file.replace(".csv", "")
            df = pd.read_csv(os.path.join(processed_path, file), sep=",", encoding="utf-8-sig")
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Tabela {table_name} criada com {len(df)} registros.")

    # Listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tabelas no banco:", tables)

    conn.close()
    return tables