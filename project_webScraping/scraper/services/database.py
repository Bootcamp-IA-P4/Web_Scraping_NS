from scraper.models import BookRecommendation
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.model = BookRecommendation

    def save_comments(self, all_comments, url):
        for comment in all_comments:
            try:
                # Convertir la fecha de texto a datetime
                date_str = comment["date"]
                try:
                    date = datetime.strptime(date_str, "%d/%m/%Y %H:%M")  # Ajusta el formato según cómo venga la fecha
                except ValueError:
                    print(f"Error al convertir la fecha: {date_str}")
                    continue
            
                self.model.objects.create(
                    author_comment = comment["author"],
                    date_comment = date,
                    content_comment = comment["content"],
                    url = url
                )
                print(f"Comentario guardado: {comment['author']} - {comment['content'][:100]}...")
            except Exception as e:
                print(f"Error al guardar el comentario: {e}")
                
