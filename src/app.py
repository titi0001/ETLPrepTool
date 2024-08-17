import io
import os
import pandas as pd
import streamlit as st
from utils.process_unit import unit_price


def main():
    st.title("Conversor de Arquivos")

    if not os.path.exists('./input_data'):
        os.makedirs('./input_data')

    opcao = st.selectbox(
        "Escolha a conversão", [
            "XLSX para CSV", "CSV para CSV"])

    arquivo_carregado = st.file_uploader(
        f"Carregue seu arquivo {
            opcao.split()[0]}", type=[
            opcao.split()[0].lower()])

    if arquivo_carregado is not None:
        try:
            nome_arquivo, _ = os.path.splitext(arquivo_carregado.name)
            caminho_csv = f'./input_data/{nome_arquivo}.csv'

            if os.path.exists(caminho_csv):
                st.warning(
                    f"O arquivo '{nome_arquivo}.csv' já existe. Por favor, carregue um arquivo diferente.")
            else:
                if opcao == "XLSX para CSV":

                    df = pd.read_excel(
                        io.BytesIO(
                            arquivo_carregado.getvalue()))

                    st.write("Pré-visualização do DataFrame Bruto")
                    st.dataframe(df, height=600)

                    df.to_csv(caminho_csv, index=False)

                    st.success(f"Arquivo salvo como {caminho_csv}")

                elif opcao == "CSV para CSV":
                    with open(caminho_csv, 'wb') as f:
                        f.write(arquivo_carregado.getbuffer())

                    df = pd.read_csv(caminho_csv)

                    unit_price(caminho_csv)

                    st.write("Pré-visualização do DataFrame Bruto")
                    st.dataframe(df, height=600)

                    df.to_csv(caminho_csv, index=False)

                    st.success(f"Arquivo salvo como {caminho_csv}")

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
    else:
        st.warning(f"Por favor, carregue um arquivo {opcao.split()[0]}.")


if __name__ == "__main__":
    main()
