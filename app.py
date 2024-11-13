import requests
from bs4 import BeautifulSoup
import time
import pandas  as pd

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
    'new_prince': new_prince,
    'installment_prince': installment_prince,
    'timestamp': timestamp

   }
    
def save_to_dataframe(product_inf, df):
    new_row = pd.DataFrame([product_inf])
    df = pd.concat([df, new_row], ignore_index=True)
    return df

if __name__ == "__main__": 

    df = pd.DataFrame()

    while True:
        page_content = fetch_page()
        produto_inf = parse_page(page_content)
        df = save_to_dataframe(produto_inf, df)
        print(df)
        time.sleep(10)
    #print(page_content)
    