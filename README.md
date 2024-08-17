# ETLPrepTool

 ### Um projeto ETL realiza o tratamento de algumas tabelas, onde um front-end é aberto utilizando o Streamlit para a importação de arquivos CSV e XLSX. Esses arquivos são convertidos para o formato CSV, e, após o tratamento dos dados, é possível subir um ambiente Docker Compose, carregando o banco de dados e populando-o com os arquivos CSV processados.

### [consultas SQL do TESTE](QUERY.md)
___

#### Passo 1: Instalar o Python e Docker (se necessário)


Se o Python não estiver instalado, você pode baixá-lo e instalá-lo a partir do site oficial do [Python](https://www.python.org/downloads/).
Se o Docker não estiver instalado, você pode baixá-lo e instalá-lo a partir do site oficial do [Docker](https://www.docker.com/products/docker-desktop/).
___


#### Passo 2: Criar um Ambiente Virtual:

```bash
python -m venv venv
```

  - 2.1 Ative o ambiente virtual:

    Windows:

    ```bash
    .venv\Scripts\activate
    ```

  - Unix:

    ```bash
    source .venv\Scripts\activate
    ```
  ___


#### Passo 3: Instalar as Bibliotecas Necessárias

```bash
pip install -r .\requirements.txt
```
___

#### Passo 4: Executar o comando para abir uma tela de front end

```bash
streamlit run app.py
```

>Porque usar o Streamlit:
>>Facilidade de Uso
>>Integração com Bibliotecas de Ciência de Dados
>>Atualização em Tempo Real
>>Compartilhamento Fácil

