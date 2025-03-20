from django.db import models

class BookRecommendation(models.Model):
    author = models.CharField(max_length=200)
    date = models.DateTimeField()
    content = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.content[:50]}..."
    
    class Meta:
        verbose_name = "Recomendación de libro"
        verbose_name_plural = "Recomendaciones de libros"
        db_table = 'comments'