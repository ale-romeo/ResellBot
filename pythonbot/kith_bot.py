from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from bs4 import BeautifulSoup
import requests

class SneakerApp(App):
    def build(self):
        self.title = "Kith Sneaker Scraper"
        self.layout = BoxLayout(orientation='vertical')

        self.textbox = TextInput(multiline=True, readonly=True)
        self.layout.add_widget(self.textbox)

        self.start_button = Button(text="Start Scraping", size_hint=(None, None))
        self.start_button.bind(on_press=self.scrape_sneaker_info)
        self.layout.add_widget(self.start_button)

        return self.layout

    def scrape_sneaker_info(self, instance):
        url = "https://kith.com/collections/sneakers"
        firefox_options = Options()
        firefox_options.add_argument("-headless")
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')


        # Define a function to update the text box with scraped information
        def update_textbox(text):
            self.textbox.text = text

        # Start scraping and update the text box
        scraped_data = ""
        for product in range(1, 100):
            sold_out = False
            product_item = soup.select_one(f'li.collection-product:nth-child({product})')
            if not product_item:
                break
            
            product_card = product_item.find(class_='product-card')
            product_title = product_card.find(class_='product-card__information').find("a").find(class_='product-card__title').text
            product_color = product_card.find(class_='product-card__information').find("a").find(class_='product-card__color').text
            product_availability = "SOLD OUT" if product_card.find(class_='product-card__information').find("a").find('span').find(class_='sold-out') else "AVAILABLE"
            
            product_link = product_card.find(class_='product-card__information').find("a")['href']

            scraped_data += f"Sneaker:\n{product_title} - {product_color} - {product_availability}\nLink: {product_link}\n\n"

        update_textbox(scraped_data)

if __name__ == '__main__':
    SneakerApp().run()
