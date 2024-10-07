import requests
from bs4 import BeautifulSoup
from google.cloud import bigquery
import csv
import gdown

def fazer_requisicao(url):
    # Faz a requisição HTTP para o site
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Erro ao acessar o site: Erro {response.status_code}")
            return None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

def extrair_links(html, url):
    #Extrais os links, o filtro tem a regra, que só pega links que forem igual a "URL" + "/" + "..."
    lista_links = []
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', href=True) 
    for link in links:
        
        href = link['href']
        
        if (href.startswith(url + '/') and href != url + '/') or 'blogs/' in href:
            lista_links.append(href)
    return lista_links
         
def rastrear(url):
    # Executa as funções de requisição, extração de links e retorna em uma lista.
    html = fazer_requisicao(url)
    lista_todos_links = extrair_links(html, url)

    for link_artigo in set(lista_todos_links):
        titulo_artigo, conteudo_artigo, autor_artigo = coletar_informacoes(link_artigo)
        if all([titulo_artigo, autor_artigo, link_artigo, conteudo_artigo]):
            lista_dados_noticia.append({
            'titulo': titulo_artigo,
            'autor': autor_artigo,
            'link': link_artigo,
            'conteudo': conteudo_artigo
        })
    gravar_dados(lista_dados_noticia)
    return True
    

def coletar_informacoes(link_artigo):
    try:
        # Faz a requisição para o artigo
        response = requests.get(link_artigo)
        if response.status_code != 200:
            #print(f"Erro na requisição: {response.status_code}")
            return None, None, None
        soup = BeautifulSoup(response.content, 'html.parser')

        # Coleta os dados
        titulo_artigo = soup.find(class_='single-header__title')
        conteudo_artigo = soup.find(class_='single-content')
        autor_artigo = soup.find(class_='author__group') or soup.find(class_='blogger__name')
        # Verifica se tem algum None
        if not all([titulo_artigo, conteudo_artigo, autor_artigo]):
            return None, None, None


        titulo_artigo = titulo_artigo.get_text(strip=True)
        conteudo_artigo = conteudo_artigo.get_text(strip=True)
        autor_artigo = autor_artigo.get_text(strip=True)

        return titulo_artigo, conteudo_artigo, autor_artigo

    except Exception as e:
        return None, None, None
 
def gravar_dados(lista_dados_noticia):
    # grava os resultados em um csv e importa o csv para a bigquery
    client = bigquery.Client.from_service_account_json('Chave.json')
    id_dataset = 'dadosnoticias'
    id_tabela = 'dados'
    
    with open('dados_noticias.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["titulo", "autor", "link", "conteudo"])
        writer.writeheader()
        writer.writerows(lista_dados_noticia)
    
    tabela_referencia = client.dataset(id_dataset).table(id_tabela)
    arquivo_csv = 'dados_noticias.csv'
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=[
        bigquery.SchemaField("titulo", "STRING"),
        bigquery.SchemaField("autor", "STRING"),
        bigquery.SchemaField("link", "STRING"),
        bigquery.SchemaField("conteudo", "STRING")
        ])
        

    with open(arquivo_csv, 'rb') as source_file:
        job = client.load_table_from_file(source_file, tabela_referencia, job_config=job_config)
        job.result()
        
    # Remove duplicadas
    query = f"""
    CREATE OR REPLACE TABLE `{id_dataset}.{id_tabela}` AS
    SELECT titulo, autor, link, conteudo
    FROM ( SELECT *, ROW_NUMBER() OVER (PARTITION BY link ORDER BY link) as row_num
        FROM `{id_dataset}.{id_tabela}`)
    WHERE row_num = 1
    """
    query_job = client.query(query)
    query_job.result()


#Inicialização dos dados: 
lista_todos_links = []
lista_dados_noticia = []
url_chave = "https://bucketarquivogns295.s3.us-east-2.amazonaws.com/chave.json"
gdown.download(url_chave, 'chave.json', quiet=True)

urls = [
    "https://www.cnnbrasil.com.br/politica",  
    "https://www.cnnbrasil.com.br/economia",
    "https://www.cnnbrasil.com.br/esportes"
]

for url in urls:
    try:
        rastreio = rastrear(url)
        print(f"Dados gravados com sucesso | {url}")    
    except:
        print(f"Não foi possivel rastrear a url {url}")
    print("Aguarde...")
print("Processo Finalizado!")
