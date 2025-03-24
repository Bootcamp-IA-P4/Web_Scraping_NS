from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from scraper.models import BookRecommendation
import time
from django.db import close_old_connections
from django.utils.timezone import make_aware
import logging
import csv
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(".webscraper.log", mode="a", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

class BookScraper:
    def __init__(self):
        self.driver = None  
        self.wait = None 
        self.url = "https://meencantaleer.es/tu-opinas/" 
        self.logger = logging.getLogger("BookScraper")

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
            time.sleep(random.uniform(0.3, 0.5))

    def get_comments(self):
        try:
            comments = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".comment-body.clearfix"))
            )
            return comments
        except TimeoutException:
            print("No se cargaron los comentarios 😒")
            return []
                
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
            self.logger.error(f"Error al extraer información del comentario: {str(e)}")
            return None
    
    def process_date(self, date_str):
        meses = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }

        try:
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
        start_time = datetime.now()
        self.logger.info("\n" + "="*50)
        self.logger.info(f"🕵️‍♂️ INICIO SCRAPING: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("="*50 + "\n")
        try:
            self.navigate_page()
            saved_comments = 0
            page_num = 1
            max_pages = 1    # Cambiar a más páginas para obtener más comentarios, de momento es para la demostración
            
            with open("comments.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["author", "date", "content"])

                while True:
                    self.logger.debug(f"\n📄 Scraping pagina {page_num} de {max_pages}...")
                    comments = self.get_comments()

                    for comment in comments:
                        info = self.extract_comment_info(comment)
                        if info:
                            try:
                                date = self.process_date(info['date'])
                                if date:
                                    close_old_connections()
                                    BookRecommendation.objects.create(
                                        author=info['author'],
                                        date=date,
                                        content=info['content'],
                                        url=self.url
                                    )
                                    writer.writerow([info['author'], date, info['content']])

                                    saved_comments += 1
                                    self.logger.info(
                                        f"📝 Comentario guardado\n"
                                        f" ├── Autor: {info['author']}\n"
                                        f" ├── Fecha: {date}\n"
                                        f" └── Contenido: {info['content'][:50]}..."
                                    )
                            except Exception as e:
                                self.logger.error(f"Error al guardar comentario: {e.__class__.__name__}")

                    self.logger.info(f"✅ [Página {page_num}] Scrapeo completado. Total guardados: {saved_comments}\n")

                    if page_num >= max_pages:
                        break

                    page_num += 1

            end_time = datetime.now()
            self.logger.info("\n📊 RESUMEN FINAL")
            self.logger.info(f"📌 Total comentarios guardados: {saved_comments}")
            self.logger.info(f"⏳ Tiempo total: {end_time - start_time}")
            self.logger.info("\n" + "="*50)
            self.logger.info("🔚 FIN DEL SCRAPING")
            self.logger.info("="*50 + "\n")

            return saved_comments
                
        except Exception as e:
            self.logger.error(f"Error al scrapear los comentarios: {e}")
            return 0
        
if __name__ == "__main__":                
    scraper = BookScraper()
    try:
        scraper.setup_driver()        
        total_saved = scraper.scrape_comments() 
    finally:
        scraper.close_driver()
        
