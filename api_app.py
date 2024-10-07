import requests
from flask import Flask, request, render_template_string, jsonify
from google.cloud import bigquery
import gdown

# Inicializa o cliente do BigQuery

url_chave = "https://bucketarquivogns295.s3.us-east-2.amazonaws.com/chave.json"
gdown.download(url_chave, 'chave.json', quiet=True)

client = bigquery.Client.from_service_account_json('chave.json')
id_dataset = 'dadosnoticias'
id_tabela = 'dados'

app = Flask(__name__)

def buscar_noticia_por_palavra(client, id_dataset, id_tabela, palavra_chave):
    query = f"""
        SELECT titulo, autor, link, conteudo
        FROM `{id_dataset}.{id_tabela}`
        WHERE LOWER(conteudo) LIKE '%{palavra_chave.lower()}%'
        OR LOWER(autor) LIKE '%{palavra_chave.lower()}%'
        OR LOWER(titulo) LIKE '%{palavra_chave.lower()}%'
        OR LOWER(link) LIKE '%{palavra_chave.lower()}%'
        LIMIT 15
    """
    
    query_job = client.query(query)  # Executa a consulta
    resultado_query = query_job.result()
    artigos = []
        
    for row in resultado_query:
        artigos.append({
            'titulo': row['titulo'],
            'autor': row['autor'],
            'link': row['link'],
            'conteudo': row['conteudo']
        })

    return artigos

def formatar_dados(artigos):
    # Formata em html, deixando mais legivel quando acessado pela API
    html_template = """
    <html>
    <body>
        <h1>Resultados da Pesquisa</h1>
        {% for artigo in artigos %}
            <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
                <h2>{{ artigo.titulo }}</h2>
                <h3>Autor: {{ artigo.autor }}</h3>
                <h3>Link: <a href="{{ artigo.link }}">{{ artigo.link }}</a></h3>
                <p>{{ artigo.conteudo }}</p>
                <hr>
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html_template, artigos=artigos)

@app.route('/buscar', methods=['GET'])
def buscar_artigos():
    palavra_chave = request.args.get('palavra_chave')
    if not palavra_chave:
        return jsonify({'erro': 'A palavra-chave é obrigatória'}), 400
    
    artigos = buscar_noticia_por_palavra(client, id_dataset, id_tabela, palavra_chave)
    if artigos:
        artigos_html = formatar_dados(artigos)
        return artigos_html, 200  # Retorna o HTML gerado
    else:
        return jsonify({'mensagem': 'Nenhum artigo encontrado para a palavra-chave fornecida'}), 404

if __name__ == '__main__':
    app.run(debug=True)
