import os
import pandas as pd
import sqlite3

def load_csvs_to_sqlite():
    # Caminho robusto baseado na localização do arquivo
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "..", "data", "nubank.db")
    processed_path = os.path.join(BASE_DIR, "..", "data", "processed")

    # Garantir que a pasta data existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Criar/abrir banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if not os.path.exists(processed_path) or not os.listdir(processed_path):
        print(f"Nenhum CSV encontrado em {processed_path}")
        conn.close()
        return []

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

if __name__ == "__main__":
    tabelas = load_csvs_to_sqlite()
    print("Tabelas carregadas:", tabelas)