from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookScraper:
    def __init__(self):
        self.driver = None  # Iniciamos en none porque no tenemos un navegador
        self.wait = None # Iniciamos en none porque inicialmente no tenemos espera
        self.url = "https://meencantaleer.es/tu-opinas/" # URL de la web que queremos scrapear

    def setup_driver(self):
        self.driver = webdriver.chrome()
        self.wait = WebDriverWait(self.driver, 10)