from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

products_available = list()

def scrape_sneaker_info():
    # URL del sito da scrapare
    url = "https://kith.com/collections/sneakers"


    # Opzioni per il driver di Firefox
    firefox_options = Options()
    firefox_options.add_argument("-headless")   # Esegui Firefox in modalità headless (senza interfaccia grafica)

    # Inizializza il driver di Firefox
    with webdriver.Firefox(options=firefox_options) as driver:
        print("BOT SCRAPER FOR KITH (\""+ url +"\")")

        # Estrai il nome del prodotto e stampa "Sold Out" o "Nope" in base alla disponibilità
        for product in range(1, 5):
            driver.get(url)
        
            while "eu.kith.com" in driver.current_url:
                driver.get(url)
            
            try:
                product_title = driver.find_element(By.XPATH, '//li[@class="collection-product"]['+str(product)+']/div[@class="product-card"]/div[@class="product-card__information"]/a/h1').text.strip()
                product_color = driver.find_element(By.XPATH, '//li[@class="collection-product"]['+str(product)+']/div[@class="product-card"]/div[@class="product-card__information"]/a/h2').text.strip()
                product_availability = driver.find_element(By.XPATH, '//li[@class="collection-product"]['+str(product)+']/div/div[@class="product-card__tag"]').text.strip()
                product_link = driver.find_element(By.XPATH, '//li[@class="collection-product"]['+str(product)+']/div/a').get_attribute('href')

                print("Sneaker:\n" + product_title + " - " + product_color + " - " + product_availability)

                if product_availability != "SOLD OUT" or product == 1:
                    print(product_link)
                    products_available.append([product_title, product_link])
                    
            except StaleElementReferenceException:
                continue
            except NoSuchElementException:
                break

    # Chiudi il driver dopo aver completato lo scraping
    driver.quit()


def scrape_single_sneaker():
    for sneaker in products_available:
        sneaker_url = sneaker[1]

        # Opzioni per il driver di Firefox
        firefox_options = Options()
        firefox_options.add_argument("-headless")   # Esegui Firefox in modalità headless (senza interfaccia grafica)

        # Inizializza il driver di Firefox
        with webdriver.Firefox(options=firefox_options) as driver:
            print("BOT SCRAPING \""+ sneaker[0] +"\"")
            print(sneaker_url)
            driver.get(sneaker_url)
            try:
                product_price = driver.find_element(By.XPATH, '//div[@class="product__shop"]/div[@class="product__price mt-12"]/span').text.strip()
                #product_color = driver.find_element(By.XPATH, '//li[@class="collection-product"]['+str(product)+']/div[@class="product-card"]/div[@class="product-card__information"]/a/h2').text.strip()
                
                print(sneaker[0] + ":\n" + product_price)
            
            except NoSuchElementException:
                print('Errore: "Nessun prezzo trovato."')
                break


if __name__ == "__main__":
    scrape_sneaker_info()
    scrape_single_sneaker()