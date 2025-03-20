from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
from scraper.models import BookRecommendation
import time
from django.db import close_old_connections
from django.utils.timezone import make_aware

class BookScraper:
    def __init__(self):
        self.driver = None  
        self.wait = None 
        self.url = "https://meencantaleer.es/tu-opinas/" 

    def setup_driver(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def navigate_page(self):
        self.driver.get(self.url)
        for _ in range(5):  
            self.driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(1)

    def get_comments(self):
        try:
            comments = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".comment-body.clearfix"))
            )
            return comments
        except TimeoutException:
            print("No se cargaron los comentarios 😒")
            return []

    def next_page(self):
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR, "div.nav-previous a")
            return True
        except NoSuchElementException:
            return False
        
    def click_next_page(self):
        try: 
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.nav-previous a"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(2)
            next_button.click()
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Error al hacer clic en 'Comentarios anteriores': {e}")
            return False
    
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
    
    def process_date(self, date_str):
        meses = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }

        try:
            date_str = date_str.replace('\n', '').strip()
            date_str = ' '.join(date_str.split())
            date_str = date_str.replace("el ", "").replace(" a las ", " ")

            parts = date_str.split()
            if len(parts) != 5:
                raise ValueError(f"Formato de fecha inesperado. Partes encontradas: {parts}")

            mes = meses[parts[0].lower()]
            dia = parts[1].replace(",", "")
            año = parts[2].replace(",", "").strip()
            hora = parts[3]
            am_pm = parts[4].lower()

            hora_parts = hora.split(":")
            hora_num = int(hora_parts[0])
            if am_pm == "pm" and hora_num != 12:
                hora_num += 12
            elif am_pm == "am" and hora_num == 12:
                hora_num = 0

            fecha_formateada = f"{año}-{mes}-{dia.zfill(2)} {hora_num:02d}:{hora_parts[1]}"
            naive_datetime = datetime.strptime(fecha_formateada, "%Y-%m-%d %H:%M")
            aware_datetime = make_aware(naive_datetime)  # Convierte a una fecha con zona horaria
            return aware_datetime
        except Exception as e:
            print(f"Error procesando fecha: {e}")
            return None

    def scrape_comments(self):
        try:
            self.navigate_page()
            saved_comments = 0
            page_num = 1
            max_pages = 2    # ponemos dos porque sino tarda mucho
            
            while True:
                print(f"\n📄 Scrapeando página {page_num} de {max_pages}...")
                comments = self.get_comments()

                for comment in comments:
                    info = self.extract_comment_info(comment)
                    if info:
                        try:
                            date = self.process_date(info['date'])
                            if date:
                                close_old_connections()
                                print(f"Guardando comentario: {info}")
                                BookRecommendation.objects.create(
                                    author=info['author'],
                                    date=date,
                                    content=info['content'],
                                    url=self.url
                                )
                                saved_comments += 1
                                print(f"Autor: {info['author']}")
                                print(f"Fecha: {date}")
                                print(f"Comentario: {info['content'][:100]}...")
                                print("-"*50)
                        except Exception as e:
                            print(f"Error al guardar comentario: {e.__class__.__name__}")
                            print(f"Datos del comentario: {info}")

                print(f"✅ Página {page_num} completada.")

                if page_num >= max_pages:
                    print(f"🏁 Alcanzado el límite de {max_pages} páginas")
                    break

                page_num += 1

            print(f"\n📊 Resumen final:")
            print(f"- Comentarios guardados exitosamente: {saved_comments}")
            return saved_comments
                
        except Exception as e:
            print(f"Error al scrapear los comentarios: {e}")
            return 0
        
if __name__ == "__main__":                
    scraper = BookScraper()
    try:
        scraper.setup_driver()        
        total_saved = scraper.scrape_comments() 
        print(f"Se guardaron {total_saved} comentarios") 
    finally:
        scraper.close_driver()
        
