function Check-Docker {
    try {
        docker --version > $null 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Docker está instalado."
        } else {
            Write-Host "Docker não está instalado. Por favor, instale o Docker antes de continuar."
            exit 1
        }
    } catch {
        Write-Host "Docker não está instalado ou não está configurado corretamente. Por favor, instale ou configure o Docker."
        exit 1
    }
}

# Verificar se o Docker está instalado
Check-Docker

# Cria um ambiente virtual na pasta .\src\.venv
python -m venv .\src\.venv

# Ativa o ambiente virtual
.\src\.venv\Scripts\Activate.ps1

# Instala as dependências do arquivo requirements.txt
pip install -r .\src\requirements.txt

# Navega até a pasta src para executar os comandos Docker e Streamlit
Set-Location -Path .\src\

# Inicia os containers Docker em segundo plano
docker compose up -d

# Executa o aplicativo Streamlit
streamlit run app.py

# Volta ao diretório original
Set-Location -Path ..\

# Mensagem de conclusão
Write-Host "Ambiente virtual criado, pacotes instalados, Docker Compose iniciado e Streamlit em execução."
