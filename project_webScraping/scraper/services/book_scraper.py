from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .database import DatabaseManager

class BookScraper:
    def __init__(self):
        self.driver = None  # Iniciamos en none porque no tenemos un navegador
        self.wait = None # Iniciamos en none porque inicialmente no tenemos espera
        self.url = "https://meencantaleer.es/tu-opinas/" # URL de la web que queremos scrapear
        self.db = DatabaseManager() 

    def setup_driver(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def navigate_page(self):
        self.driver.get(self.url)

    def get_comments(self):
        try:
            comments = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".comment-body.clearfix"))
            )
            return comments
        except TimeoutException:
            print("No se cargaron los comentarios 😒")
            return []

    def extract_comment_info(self, comment):
        try:
            author = comment.find_element(By.CLASS_NAME, "fn").text
            date = comment.find_element(By.CLASS_NAME, "comment_date").text
            content = comment.find_element(By.CSS_SELECTOR, ".comment-content.clearfix p").text
            return {
                "author": author,
                "date": date,
                "content": content
            }
        except Exception as e:
            print(f"Error al extraer información del comentario: {e}")
            return None

    def scrape_comments(self):
        try:
            self.navigate_page() #navega a la página
            comments = self.get_comments() #obtenemos los comentarios

            all_comments = [] #lista para guardar los comentarios
            for comment in comments:   #iteramos sobre los comentarios
                info = self.extract_comment_info(comment)
                if info: #si la información es correcta
                    all_comments.append(info)
                    print(f"Autor: {info['author']}")
                    print(f"Fecha: {info['date']}")
                    print(f"Comentario: {info['content'][:100]}...")
                    print("-"*50)

            self.db.save_comments(all_comments, self.url)
            return all_comments
        except Exception as e:
            print(f"Error al scrapear los comentarios: {e}")
            return []
        
if __name__ == "__main__":                #crea una instancia del scraper
    scraper = BookScraper()
    try:
        scraper.setup_driver()           #inicia el navegador
        results = scraper.scrape_comments() #ejecuta el scrapeo
        print(f"Se scrapearon {len(results)} comentarios") #imprime el número de comentarios scrapeados
    finally:
        scraper.close_driver()
