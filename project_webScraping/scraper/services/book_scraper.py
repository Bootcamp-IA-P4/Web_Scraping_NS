from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from database import DatabaseManager
import time

class BookScraper:
    def __init__(self):
        self.driver = None  # Iniciamos en none porque no tenemos un navegador
        self.wait = None # Iniciamos en none porque inicialmente no tenemos espera
        self.url = "https://meencantaleer.es/tu-opinas/" # URL de la web que queremos scrapear
        self.db = DatabaseManager() 

    def setup_driver(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

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
            self.navigate_page()
            all_comments = []
            page_num = 1
            
            while True:
                print(f"\n📄 Scrapeando página {page_num}...")
                comments = self.get_comments()

                for comment in comments:
                    info = self.extract_comment_info(comment)
                    if info:
                        all_comments.append(info)
                        print(f"Autor: {info['author']}")
                        print(f"Fecha: {info['date']}")
                        print(f"Comentario: {info['content'][:100]}...")
                        print("-"*50)
                print(f"✅ Página {page_num} completada. Comentarios encontrados: {len(comments)}")

                if not self.next_page():
                    print("🏁 No hay más páginas para scrapear")
                    break

                if not self.click_next_page():
                    print("🏁 No se pudo hacer clic en 'Comentarios anteriores'")
                    break

                page_num += 1

            self.db.save_comments(all_comments, self.url)
            return all_comments
                
        except Exception as e:
            print(f"Error al scrapear los comentarios: {e}")
            return []

    def search_comments(self, keyword):
        try:
            print(f"\n🔍 Buscando comentarios con la palabra clave: '{keyword}'...")
            
            # Navegar a la página principal
            self.navigate_page()
            
            # Encontrar el campo de búsqueda
            search_input = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "search-field"))
            )
            
            # Limpiar el campo y escribir la palabra clave
            search_input.clear()
            search_input.send_keys(keyword)
            
            # Enviar la búsqueda
            search_input.submit()
            
            # Esperar a que carguen los resultados
            time.sleep(2)
            
            # Obtener y procesar los comentarios encontrados
            search_results = []
            page_num = 1
            
            while True:
                print(f"\n📄 Procesando página {page_num} de resultados...")
                comments = self.get_comments()
                
                for comment in comments:
                    info = self.extract_comment_info(comment)
                    if info:
                        # Añadir la palabra clave de búsqueda al documento
                        info['search_keyword'] = keyword
                        search_results.append(info)
                        print(f"Autor: {info['author']}")
                        print(f"Fecha: {info['date']}")
                        print(f"Comentario: {info['content'][:100]}...")
                        print("-"*50)
                
                print(f"✅ Página {page_num} completada. Resultados encontrados: {len(comments)}")
                
                # Verificar si hay más páginas de resultados
                if not self.next_page():
                    print("🏁 No hay más páginas de resultados")
                    break
                
                if not self.click_next_page():
                    print("🏁 No se pudo acceder a la siguiente página")
                    break
                
                page_num += 1
            
            # Guardar los resultados en la base de datos
            if search_results:
                self.db.save_comments(search_results, self.url)
                print(f"\n✨ Se encontraron y guardaron {len(search_results)} comentarios relacionados con '{keyword}'")
            else:
                print(f"\n❌ No se encontraron comentarios relacionados con '{keyword}'")
            
            return search_results
            
        except Exception as e:
            print(f"Error durante la búsqueda: {e}")
            return []

if __name__ == "__main__":
    scraper = BookScraper()
    try:
        if scraper.db.connection_test():
            scraper.setup_driver()
            
            # Ejemplo de uso del buscador
            keyword = input("Introduce una palabra clave para buscar (o presiona Enter para scrapear todo): ").strip()
            
            if keyword:
                results = scraper.search_comments(keyword)
                print(f"Se encontraron {len(results)} comentarios relacionados con '{keyword}'")
            else:
                results = scraper.scrape_comments()
                print(f"Se scrapearon {len(results)} comentarios en total")
    finally:
        scraper.close_driver()
        scraper.db.close_connection()
