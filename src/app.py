import io
import os
import pandas as pd
import streamlit as st
from utils.process_unit import unit_price
from utils.move_files import mover_arquivos
from utils.query_utils import executar_query  # Importando a função criada


def main():
    st.title("Conversor de Arquivos e Consulta SQL- Ambiente de Desenvolvimento")

    # Verifica se os diretórios necessários existem e os cria se não existirem
    if not os.path.exists("./input_data"):
        os.makedirs("./input_data")

    # Criando uma barra lateral para navegação
    menu = ["Conversão de Arquivos", "Consulta SQL"]
    escolha = st.sidebar.selectbox("Escolha uma opção", menu)

    if escolha == "Conversão de Arquivos":
        st.header("Conversão de Arquivos xls-xlsx/csv")

        opcao = st.selectbox("Escolha a conversão", ["XLSX para CSV", "CSV para CSV"])

        if opcao is not None:
            arquivo_carregado = st.file_uploader(
                f"Carregue seu arquivo {opcao.split()[0]}",
                type=[opcao.split()[0].lower()],
            )
        else:
            arquivo_carregado = None

        if arquivo_carregado is not None:
            try:
                nome_arquivo, _ = os.path.splitext(arquivo_carregado.name)
                caminho_csv = f"./input_data/{nome_arquivo}.csv"

                if os.path.exists(caminho_csv):
                    st.warning(
                        f"O arquivo '{nome_arquivo}.csv' já existe. Por favor, carregue um arquivo diferente."
                    )
                else:
                    if opcao == "XLSX para CSV":
                        df = pd.read_excel(io.BytesIO(arquivo_carregado.getvalue()))

                        st.write("Pré-visualização do DataFrame Bruto")
                        st.dataframe(df, height=600)

                        df.to_csv(caminho_csv, index=False)

                        st.success("Arquivo salvo")

                    elif opcao == "CSV para CSV":
                        with open(caminho_csv, "wb") as f:
                            f.write(arquivo_carregado.getbuffer())

                        df = pd.read_csv(caminho_csv)

                        unit_price(caminho_csv)

                        st.write("Pré-visualização do DataFrame Bruto")
                        st.dataframe(df, height=300)

                        df.to_csv(caminho_csv, index=False)

                        st.success("Arquivo salvo")

            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {e}")

        # Adicionando um botão para mover os arquivos e executar o DB
        st.write("Aplicar ELT e executar o DB após carregar todos os arquivos")
        if st.button("ELT e executar o DB"):
            mover_arquivos()

    elif escolha == "Consulta SQL":
        st.header("Consulta SQL Dinâmica com PostgreSQL")

        # Campo de input para a consulta SQL completa
        consulta_sql = st.text_area("Insira sua consulta SQL:", height=200)

        # Quando o botão é clicado, executar a consulta SQL
        # Quando o botão é clicado, executar a consulta SQL
        if st.button("Executar Consulta"):
            if consulta_sql.strip():
                df = executar_query(consulta_sql)

                # Exibir os resultados da consulta
                if df is not None and not df.empty:
                    st.dataframe(df)
                else:
                    st.write("Nenhum resultado encontrado.")
            else:
                st.write("Por favor, insira uma consulta SQL válida.")


if __name__ == "__main__":
    main()
