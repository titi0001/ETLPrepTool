import os
import shutil
import pandas as pd
from sqlalchemy import create_engine, text


def converter_colunas_para_minusculas(df):
    df.columns = df.columns.str.lower()
    return df


def mover_arquivos():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    src_dir = os.path.join(base_dir, "../")
    input_dir = os.path.join(src_dir, "input_data")
    staging_dir = os.path.join(src_dir, "staging_data")
    processed_dir = os.path.join(src_dir, "data")

    os.makedirs(processed_dir, exist_ok=True)

    if not os.listdir(input_dir) and not os.listdir(staging_dir):
        print("Nenhum arquivo para processar.")
        return

    for file_name in os.listdir(input_dir):
        src_path = os.path.join(input_dir, file_name)
        dest_path = os.path.join(processed_dir, file_name)
        print(f"Movendo {file_name} para {processed_dir}")
        shutil.move(src_path, dest_path)

    for file_name in os.listdir(staging_dir):
        src_path = os.path.join(staging_dir, file_name)
        dest_path = os.path.join(processed_dir, file_name)
        print(f"Movendo {file_name} para {processed_dir}")
        shutil.move(src_path, dest_path)

    db_user = os.getenv("DB_USER", "admin")
    db_password = os.getenv("DB_PASSWORD", "admin")
    db_name = os.getenv("DB_NAME", "crm")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")

    engine = create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    # Conexão ao banco de dados e processamento dos arquivos CSV
    with engine.connect() as connection:
        for filename in os.listdir(processed_dir):
            if filename.endswith(".csv"):
                table_name = os.path.splitext(filename)[0].lower()

                csv_path = os.path.join(processed_dir, filename)

                print(f"Lendo arquivo {csv_path}")
                df = pd.read_csv(csv_path)

                df = converter_colunas_para_minusculas(df)

                try:
                    query = text(
                        f"""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = '{table_name}'
                    """
                    )
                    expected_columns = set(row[0] for row in connection.execute(query))

                    df_columns = set(df.columns)

                    if not df_columns.issubset(expected_columns):
                        raise ValueError(
                            f"Colunas do DataFrame não correspondem às colunas da tabela {table_name}"
                        )

                    # Insere os dados na tabela existente no banco de dados
                    print(f"Inserindo dados na tabela {table_name}")
                    df.to_sql(table_name, engine, if_exists="append", index=False)
                    print(f"Dados inseridos com sucesso na tabela {table_name}")

                except ValueError as e:
                    print(f"Erro ao processar o arquivo {filename}: {e}")
