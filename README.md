# Abaixo segue o resumo da função dos apps dentro desse projeto

# coletor_app.py
Coleta as noticias de um site e grava na BigQuery.

# api_app.py
Disponibiliza as informações gravas na BigQuery (Google Cloud)  para consulta via api.
Atualmente, a api esta usando host local "http://127.0.0.1:5000/"
Para buscar uma palavra, basta acessar pelo navegador dessa forma: 

"http://127.0.0.1:5000/buscar?palavra_chave=" + palavra que deseja pesquisar. 


