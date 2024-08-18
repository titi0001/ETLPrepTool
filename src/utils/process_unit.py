import os
import pandas as pd


def unit_price(caminho_csv):
    """
    Função para processar o campo 'UnitPrice' em um arquivo CSV.
    Remove o símbolo de moeda 'R$', os espaços em branco à esquerda,
    as aspas duplas e substitui a vírgula por ponto.
    """
    df = pd.read_csv(caminho_csv)

    def preencher_vazios_com_null(df):
        """
        Função para preencher valores vazios na coluna 'ProductDetail' com 'NULL'.
        """
        if "ProductDetail" in df.columns:
            df["ProductDetail"] = df["ProductDetail"].apply(
                lambda x: "NULL" if pd.isna(x) or x.strip() == "" else x
            )
        else:
            print("A coluna 'ProductDetail' não foi encontrada")
        return df

    if "UnitPrice" in df.columns:
        for i in range(len(df)):
            valor_original = df.at[i, "UnitPrice"]

            try:
                valor_limpo = valor_original.replace("R$", "").replace('"', "").lstrip()
                valor_limpo = valor_limpo.replace(",", ".")

                df.at[i, "UnitPrice"] = valor_limpo

            except Exception as e:
                print(f"Erro ao processar o valor {valor_original}: {e}")

        df = preencher_vazios_com_null(df)
        
        caminho_saida = "./src/staging_data"
        os.makedirs(caminho_saida, exist_ok=True)

        nome_arquivo = os.path.basename(caminho_csv)
        caminho_csv_modificado = os.path.join(caminho_saida, nome_arquivo)

        df.to_csv(caminho_csv_modificado, index=False)

        return df

    else:
        print("A coluna 'UnitPrice' não foi encontrada no arquivo.")
        return df
