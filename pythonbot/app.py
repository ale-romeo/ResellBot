from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def index():
    scraped_data = scrape_sneaker_info()
    return render_template('index.html', scraped_data=scraped_data)

def scrape_sneaker_info():
        url = "https://kith.com/collections/sneakers"
        firefox_options = Options()
        firefox_options.add_argument("-headless")
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')


        # Start scraping and update the text box
        scraped_data = []
        for product in range(1, 100):
            sold_out = False
            product_item = soup.select_one(f'li.collection-product:nth-child({product})')
            if not product_item:
                break
            
            product_card = product_item.find(class_='product-card')
            product_title = product_card.find(class_='product-card__information').find("a").find(class_='product-card__title').text
            product_color = product_card.find(class_='product-card__information').find("a").find(class_='product-card__color').text
            product_availability = "SOLD OUT" if product_card.find(class_='product-card__information').find("a").find('span').find(class_='sold-out') else "AVAILABLE"
            
            product_link = "https://kith.com" + product_card.find(class_='product-card__information').find("a")['href']

            sneaker_info = {
                'title': product_title,
                'color': product_color,
                'availability': product_availability,
                'link': product_link
            }

            scraped_data.append(sneaker_info)

        return scraped_data

if __name__ == '__main__':
    app.run(debug=True)
