from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os 

class DatabaseManager:
    def __init__(self):
        load_dotenv()

        try:
            self.client = MongoClient(os.getenv('DB_URI'))
            self.db = self.client['web_scraping']
            self.collection = self.db['comments']
            print(f" 💕 Conectado a la base de datos: {self.db.name}")
            print(f" 💕 Usando colección: {self.collection.name}")
        except Exception as e:
            print(f"Error al inicializar la conexión: {e}")

    def connection_test(self):
        try:
            self.client.admin.command('ping')
            print("Conexión exitosa con MongoDB!")
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False

    def save_comments(self, all_comments, url):
        saved_comments = 0
        #print(f"\n🔄 Intentando guardar {len(all_comments)} comentarios...")
        
        # Diccionario para convertir nombres de meses en español a números
        meses = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }
        
        for i, comment in enumerate(all_comments, 1):
            try:
                # Procesar la fecha
                date_str = comment["date"]
                try:
                    # Limpiar el string de la fecha de cualquier HTML y espacios extra
                    date_str = date_str.replace('\n', '').strip() #elimina los saltos de linea y espacios extra
                    date_str = ' '.join(date_str.split())  # Normalizar espacios
                    
                    # Eliminar "el" y "a las" del string
                    date_str = date_str.replace("el ", "").replace(" a las ", " ")
                    #print(f"Fecha limpia: {date_str}")  # Debug
                    
                    # Separar la fecha en partes
                    parts = date_str.split()
                    if len(parts) != 5:
                        raise ValueError(f"Formato de fecha inesperado. Partes encontradas: {parts}")
                    
                    mes = meses[parts[0].lower()]
                    dia = parts[1].replace(",", "")
                    año = parts[2].replace(",", "").strip()
                    hora = parts[3]
                    am_pm = parts[4].lower()
                    
                    # Convertir hora a formato 24h si es necesario
                    hora_parts = hora.split(":")
                    hora_num = int(hora_parts[0])
                    if am_pm == "pm" and hora_num != 12:
                        hora_num += 12
                    elif am_pm == "am" and hora_num == 12:
                        hora_num = 0
                    
                    # Crear string de fecha en formato correcto
                    fecha_formateada = f"{año}-{mes}-{dia.zfill(2)} {hora_num:02d}:{hora_parts[1]}"
                    date = datetime.strptime(fecha_formateada, "%Y-%m-%d %H:%M")
                    
                    comment_doc = {
                        "author": comment["author"],
                        "date": date,
                        "content": comment["content"],
                        "url": url,
                        "created_at": datetime.now()
                    }

                    result = self.collection.insert_one(comment_doc)
                    saved_comments += 1
                    
                except Exception as e:
                    continue
                
            except Exception as e:
                print(f"Error al guardar el comentario: {str(e)}")
                
        print(f"\n📊 Resumen final:")
        print(f"- Total de comentarios a procesar: {len(all_comments)}")
        print(f"- Comentarios guardados exitosamente: {saved_comments}")
        print(f"- Comentarios no guardados: {len(all_comments) - saved_comments}")

    def close_connection(self):
        self.client.close()
        print("🔚Conexión cerrada con MongoDB!")
