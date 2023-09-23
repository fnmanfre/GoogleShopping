from typing import Any
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Sel:
     '''Selector class'''
     GROUP_RESULT = 'sh-sr__shop-result-group'
     PRODUTC_CONTENT = 'sh-dgr__content'
     PRODUTC = 'tAxDx'
     PRICE = 'XrAfOe'
     SELLER = 'aULzUe'
     RATE = 'NzUzee'
     VALUE = 'QIrs8'
     LINK = 'C7Lkve'
     

class GoogleShoppingScraping:
    '''Class for web scraping Google Shopping and returning a list of results containing a dictionary with product name, price, seller, rating, and store link.'''

    def __init__(self, headless: bool = True, implicitly_wait: float = 0.5) -> None:
        self.headless = headless
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if self.headless:
            self.chrome_options.add_argument('--headless=new')
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=self.chrome_options, service=self.service)
        self.driver.implicitly_wait(implicitly_wait)
        self.results = []

    def _load_page(self):

        URL = r'https://shopping.google.com/?nord=1&pli=1'

        try:
            self.driver.get(URL)
            
        except Exception as e:
            print(f'Google page is not available: {e.__class__.__name__} ')
            raise e

    def _input(self, search):
            assert isinstance(search, str)

            self.driver.find_element(By.ID, 'REsRA').send_keys(search, Keys.ENTER)
            target = By.CLASS_NAME, Sel.GROUP_RESULT
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(target))

           
    def _scraping(self):

        list_results = self.driver.find_elements(By.CLASS_NAME, Sel.PRODUTC_CONTENT)

        for result in list_results:
            
            try:
                product = result.find_element(By.CLASS_NAME, Sel.PRODUTC).text
                price = result.find_element(By.CLASS_NAME, Sel.PRICE).find_element(
                    By.CLASS_NAME, Sel.VALUE).text
                seller = result.find_element(By.CLASS_NAME, Sel.SELLER).text
                
                try:
                    rate = result.find_element(By.CLASS_NAME, Sel.RATE).find_element(
                        By.CLASS_NAME, Sel.VALUE).text
                
                except NoSuchElementException:
                    rate = 'no reviews'
                
                link = result.find_element(By.CLASS_NAME, Sel.LINK).find_element(
                    By.TAG_NAME, 'a').get_attribute('href')
                offer = {
                    'product' : product.strip(),
                    'price' : price.strip(),
                    'seller' : seller.strip(),
                    'rate' : rate.strip(),
                    'link' : link,
                }

                self.results.append(offer)

            except:
                pass
        
    def __call__(self,  search: str) -> list:
        self._load_page()
        self._input(search)
        self._scraping()

        return self.results
         


if __name__ == '__main__':

    # IMPLEMENTATION EXAMPLE
    search = input("What are you looking for?? \n>> ")
    print('Please wait a minute')
    example = GoogleShoppingScraping(headless=True, implicitly_wait=0.1)
    search_results = example(search)

    for i, r in enumerate(search_results):
        print()
        print(f'Result {i+1}')
        for k, v in r.items():
            print(k,': ', v)
        print()

    