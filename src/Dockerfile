# Use a imagem base do Jupyter com SciPy
FROM jupyter/scipy-notebook:latest

# Mudar para o usuário root para instalar pacotes
USER root

# Atualizar a lista de pacotes e instalar o libpq-dev
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Retornar ao usuário padrão do Jupyter
USER $NB_UID
