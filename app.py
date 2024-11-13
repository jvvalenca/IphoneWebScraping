import requests

def fetch_page():
    url = "https://www.mercadolivre.com.br/apple-iphone-16-pro-max-1-tb-titnio-preto-distribuidor-autorizado/p/MLB1040287854#polycard_client=search-nordic&wid=MLB5093482120&sid=search&searchVariation=MLB1040287854&position=8&search_layout=stack&type=product&tracking_id=1c14efda-e073-476c-b8fc-0b889df5a121"
    response = requests.get(url)
    return(response.text)

if __name__ == "__main__":
    
    page_content = fetch_page()
    print(page_content)