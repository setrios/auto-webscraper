import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from pydantic_models import CarListing



class ListCrawler():
    def __init__(self, href):
        self.list_view_href = href
        self.page_num = int(re.search(r'page=([0-9]+)', href).group(1))
        self.hrefs = []
        self.page_was_full = True

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.ctx = ctx

    def __get_all_hrefs_on_page(self):
        print(f'Retrieving: {self.list_view_href}')

        html = urllib.request.urlopen(self.list_view_href, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')

        tags = soup.select('a.link.product-card')
        # tags = soup.select('div#items > div > a.link.product-card')  # skip the day offer

        relative_hrefs = [tag['href'] for tag in tags]
        absolute_hrefs = ['https://auto.ria.com' + rh for rh in relative_hrefs]
        if absolute_hrefs:
            self.hrefs += absolute_hrefs
            self.page_was_full = True
        else:
            self.page_was_full = False

    def __go_to_next_page(self):
        self.page_num += 1

        page_num_str = str(self.page_num)

        self.list_view_href = self.list_view_href[:-len(page_num_str)] + str(self.page_num)

    def get_all_hrefs(self, pages_to_scrap):
        scrape_all = pages_to_scrap < 0
        
        while self.page_was_full:
            if not scrape_all and self.page_num >= pages_to_scrap:
                break
            
            self.__get_all_hrefs_on_page()
            self.__go_to_next_page()
        
        return self.hrefs



class DetailCrawler():
    def __init__(self, hrefs):
        self.hrefs = hrefs
        self.cars = []

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.ctx = ctx

    def get_all_info(self):
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.set_preference('dom.webdriver.enabled', False)
        firefox_options.set_preference('useAutomationExtension', False)
        firefox_options.add_argument('--width=1920')  # for phone button to be in a viewport
        firefox_options.add_argument('--height=1080') # for phone button to be in a viewport

        self.driver = webdriver.Firefox(options=firefox_options)

        try:
            for href in self.hrefs:
                self.__get_info_from_page(href)
        finally:
            if self.driver:
                self.driver.quit()

        return self.cars

    def __get_info_from_page(self, href):
        print(f'Getting info of: {href}')

        html = urllib.request.urlopen(href, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        car_data = {
            'url': href,
            'title': self.__get_title(soup),
            'price_usd': self.__get_price_usd(soup),
            'odometer': self.__get_odometer(soup),
            'username': self.__get_username(soup),
            'phone_number': self.__get_phone_number(href),
            'image_url': self.__get_first_image_url(soup),
            'images_count': self.__get_images_count(soup),
            'car_number': self.__get_car_number(soup),
            'car_vin': self.__get_car_vin(soup)
        }
        
        car = CarListing(**car_data)  # validate
        print(car)
        self.cars.append(car)
    
        
    def __get_title(self, soup):
        title_div = soup.find('div', id='sideTitleTitle')
        if title_div and title_div.span:
            return title_div.span.text
        
        return None
    
    def __get_price_usd(self, soup):
        price_div = soup.find('div', id='sidePrice')
        if price_div and price_div.strong:
            return price_div.strong.text
        
        return None
    
    def __get_odometer(self, soup):
        odometer_div = soup.find('div', id='basicInfoTableMainInfo0')
        if odometer_div and odometer_div.span:
            return odometer_div.span.text
        
        return None
    
    def __get_username(self, soup):
        username_div = soup.find('div', id='sellerInfoUserName')
        if username_div and username_div.span:
            return username_div.span.text
        
        return None
    
    def __get_images_count(self, soup):
        photo_slider = soup.find('div', id='photoSlider')
        if photo_slider:
            badge = photo_slider.find('span', class_='common-badge')
            if badge:
                spans = badge.find_all('span')
                if spans:
                    return spans[-1].text
                
        return None
    
    def __get_car_number(self, soup):
        car_number_div = soup.find('div', class_='car-number')
        if car_number_div and car_number_div.span:
            return car_number_div.span.text
        
        return None
    
    def __get_car_vin(self, soup):
        vin_span = soup.find('span', id='badgesVin')
        if vin_span and vin_span.span:
            return vin_span.span.text
        
        return None
    
    def __get_first_image_url(self, soup):
        active_slide = soup.find('li', class_='carousel__slide--active')
        
        if active_slide:
            img = active_slide.find('img')
            if img:
                # src first, data-src as fallback
                return img.get('src') or img.get('data-src') or ''
        
        return None

    def __get_phone_number(self, url):
        try:
            self.driver.get(url)

            # self.driver.save_screenshot('debug_after_load.png')
            
            wait = WebDriverWait(self.driver, 0.1)
            
            phone_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.conversion[data-action="showBottomPopUp"]'))
            )

            phone_button.click()
            
            actual_number_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.conversion[data-action="call"] span'))
            )
            
            phone_number = actual_number_element.text.strip()

            return phone_number
        
        except:
            return None
    





        