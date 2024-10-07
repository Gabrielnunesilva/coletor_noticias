# Coletor Noticias

# Descrição do projeto:

Este repositório tem como objetivo, encontrar uma solução para fazer a raspagem de um site de noticias, limpar os dados e armazenar no BigQuery (Google Cloud) e os disponibiliza para pesquisa via API> 

# Desenvolvimento

O programa foi desenvolvimento em Python, utilizando algumas bibliotecas como beautifulsoup4, google-cloud-bigquery, Flask, requests, google-auth e gdown.

# Credenciais

As credencias para acesso a BigQuery estão armazenadas em uma fonte externa (Bucket Aws), durante a execução dos arquivos, é feito o download das credencias para a pasta local do projeto. 

# Como instalar:
1- Clone o repositório:
git https://github.com/Gabrielnunesilva/coletor_noticias.git

2- Entre na pasta do repositório que você acabou de clonar:
cd coletor_noticias

3- Instale as dependências dos projeto:
pip install -r requirements.txt

4- Execute o arquivo:
Para coletar as noticias, execute o app coletor_app.py  
Para executar a API, execute o api_app.py

# Sobre api_app.py
Disponibiliza as informações gravas na BigQuery (Google Cloud)  para consulta via api
Acesse o link abaixo, com a palavra a ser pesquisada para testar a API:
http://127.0.0.1:5000/buscar?palavra_chave=


