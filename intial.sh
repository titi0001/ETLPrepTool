#!/bin/bash

# Função para verificar se o Docker está instalado
function check_docker {
    if command -v docker >/dev/null 2>&1; then
        echo "Docker está instalado."
    else
        echo "Docker não está instalado. Por favor, instale o Docker antes de continuar."
        exit 1
    fi
}

# Verificar se o Docker está instalado
check_docker

# Criar um ambiente virtual na pasta ./src/.venv
python3 -m venv ./src/.venv

# Ativar o ambiente virtual
source ./src/.venv/bin/activate

# Instalar as dependências do arquivo requirements.txt
pip install -r ./src/requirements.txt

# Iniciar os containers Docker em segundo plano
docker compose up -d

# Executar o aplicativo Streamlit
streamlit run app.py

# Mensagem de conclusão
echo "Ambiente virtual criado, pacotes instalados, Docker Compose iniciado e Streamlit em execução."
