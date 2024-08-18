import io
import os
import pandas as pd
import streamlit as st
from utils.process_unit import unit_price
from utils.move_files import mover_arquivos


def main():
    st.title("Conversor de Arquivos xls-xlsx/csv")

    if not os.path.exists("./input_data"):
        os.makedirs("./input_data")

    opcao = st.selectbox("Escolha a conversão", ["XLSX para CSV", "CSV para CSV"])

    if opcao is not None:
        arquivo_carregado = st.file_uploader(
            f"Carregue seu arquivo {
                opcao.split()[0]}",
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
                    f"""O arquivo '{nome_arquivo}.csv'
                    já existe. Por favor, carregue um arquivo diferente."""
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

    # Adicionando um botão
    st.write("Aplicar ELT e executar o DB apos carregar os todos os arquivos")
    if st.button("ELT e executar o DB"):
        mover_arquivos()


if __name__ == "__main__":
    main()
