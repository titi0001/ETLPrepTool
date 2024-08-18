import psycopg2
import pandas as pd


def executar_query(query, params=None):
    """
    Função para executar uma consulta SQL no PostgreSQL.

    Args:
        query (str): A consulta SQL a ser executada.
        params (tuple): Parâmetros para a consulta SQL.

    Returns:
        pd.DataFrame: Resultado da consulta como um DataFrame.
    """
    try:
        # Conexão com o banco de dados PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            database="crm",
            user="admin",
            password="admin",
        )

        with conn.cursor() as cursor:
            cursor.execute(query, params)

            if query.strip().upper().startswith(("SELECT", "WITH")):
                data = cursor.fetchall()

                if cursor.description is not None:
                    columns = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(data, columns=columns)
                else:
                    df = pd.DataFrame(data)

                return df
            else:
                conn.commit()
                return None

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
        return None

    finally:
        if conn is not None:
            conn.close()
