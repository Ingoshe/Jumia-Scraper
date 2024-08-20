import requests
from bs4 import BeautifulSoup
import csv


def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def extract_product_details(product):
    try:
        name = product.find('h3', class_='name').get_text(strip=True)
    except AttributeError:
        name = 'N/A'
    
    try:
        brand = product.find('div', class_='brand').get_text(strip=True)
    except AttributeError:
        brand = 'N/A'
    
    try:
        price = product.find('div', class_='prc').get_text(strip=True)
    except AttributeError:
        price = 'N/A'
    
    try:
        discount = product.find('div', class_='bdg _dsct _sm').get_text(strip=True).replace('Discount', '').strip()
    except AttributeError:
        discount = 'N/A'
    
    try:
        reviews = product.find('span', class_='rev').get_text(strip=True)
    except AttributeError:
        reviews = '0'
    
    try:
        rating = product.find('div', class_='stars').get('title', '0').split()[0]
    except AttributeError:
        rating = '0'
    
    return [name, brand, price, discount, reviews, rating]

# Main function to scrape the deals of the week
def scrape_jumia_deals():
    base_url = 'https://www.jumia.co.ke/'
    deals_url = base_url + 'recommended/'
    
    soup = fetch_page(deals_url)
    if soup is None:
        return

    products = soup.find_all('article', class_='prd')
    
    with open('jumia_deals.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Brand Name', 'Price (Ksh)', 'Discount (%)', 'Total Number of Reviews', 'Product Rating (out of 5)'])
        
        for product in products:
            details = extract_product_details(product)
            writer.writerow(details)
    
    print("Scraping completed. Data saved to 'jumia_deals.csv'.")


if __name__ == '__main__':
    scrape_jumia_deals()





