import requests
from bs4 import BeautifulSoup
import time
import pandas  as pd
import sqlite3

def fetch_page():
    url = "https://www.mercadolivre.com.br/apple-iphone-16-pro-max-1-tb-titnio-preto-distribuidor-autorizado/p/MLB1040287854#polycard_client=search-nordic&wid=MLB5093482120&sid=search&searchVariation=MLB1040287854&position=8&search_layout=stack&type=product&tracking_id=1c14efda-e073-476c-b8fc-0b889df5a121"
    response = requests.get(url)
    return(response.text)


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('h1', class_='ui-pdp-title').get_text()
    princes: list  = soup.find_all('span', class_='andes-money-amount__fraction')
    old_price: int =  int(princes[0].get_text().replace('.', ''))
    new_prince: int = int(princes[1].get_text().replace('.', ''))
    installment_prince: int = int(princes[2].get_text().replace('.', ''))
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    return{
    
    'product_name': product_name,
    'old_price': old_price,
    'new_price': new_prince,
    'installment_price': installment_prince,
    'timestamp': timestamp

   }

def create_connection(db_name='iphone_prices.db'):
    """Cria uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(db_name)
    return conn

def setup_database(conn):
    """Cria a tabela de preços se ela não existir."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            old_price INTEGER,
            new_price INTEGER,
            installment_price INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()


def save_to_database(conn, product_inf):
    new_row = pd.DataFrame([product_inf])
    new_row.to_sql('prices', conn, if_exists='append', index=False)


def get_max_price(conn):
    #conectar com o banco
    cursor = conn.cursor()
    #preço máximo histórico (Select max(price))
    cursor.execute("SELECT MAX(new_price), timestamp FROM prices")
    #retornar esse valor
    result = cursor.fetchone()
    return result[0], result[1]
    

if __name__ == "__main__": 
    conn = create_connection()
    setup_database(conn)
    

    while True:

        page_content = fetch_page()
        produto_inf = parse_page(page_content)

        max_price, max_timestamp = get_max_price(conn)

        current_price = produto_inf["new_price"]

        max_price_timestamp = None

        if current_price > max_price:
            print("Preço maior detectado")
            max_price = current_price
            max_price_timestamp = produto_inf('timestamp')
        else: 
            print(f"O maior preço registrado é {max_price} em {max_price_timestamp}")

        save_to_database(conn, produto_inf)
        print("Dados salvos do banco de dados: ", produto_inf)
        time.sleep(10)
    #print(page_content)
   
   
    