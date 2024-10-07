# Coletor Noticias

## Descrição do projeto:

Este repositório tem como objetivo, encontrar uma solução para fazer a raspagem de um site de noticias, limpar os dados e armazenar no BigQuery (Google Cloud) e os disponibiliza para pesquisa via API.
>Nesse projeto, estaremos utilizando como base alguns links do site [`CNN Brasil`](https://www.cnnbrasil.com.br)


<br />

# Desenvolvimento

O programa foi desenvolvimento em Python, utilizando algumas bibliotecas como beautifulsoup4, google-cloud-bigquery, Flask, requests, google-auth e gdown.
>Mais abaixo, é instruido como instalar as depêndencias para executar os programas. 

<br />

# Credenciais

As credencias para acesso a BigQuery estão armazenadas em uma fonte externa (Bucket Aws), durante a execução dos arquivos, é feito o download das credencias para a pasta local do projeto. 
>Como é apenas uma base teste, não há problemas em expor a credencial. Caso esteja utilizando uma base real, ou com dados sensiveis, lembre-se de utilizar um meio para a chave segura, como o Google Secret Manager.

<br />

# Como instalar:
1- Clone o repositório:
```sh
git https://github.com/Gabrielnunesilva/coletor_noticias.git
```

2- Entre na pasta do repositório que você acabou de clonar:
```sh
cd coletor_noticias
```

3- Instale as dependências dos projeto:
```sh
pip install -r requirements.txt
```
<br />

4- Execute o arquivo:
<br />
Para coletar as noticias, execute o app coletor_app.py  
<br />
Para pesquisar por API,  execute o api_app.py
<br />

# Sobre api_app.py
Disponibiliza as informações gravas na BigQuery (Google Cloud)  para consulta via api
Acesse o link abaixo, com a palavra a ser pesquisada para testar a API:
```sh
http://127.0.0.1:5000/buscar?palavra_chave=
```
>



