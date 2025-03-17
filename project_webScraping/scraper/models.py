from django.db import models

class BookRecommendation(models.Model):
    author_comment = models.CharField(max_length=200)
    date_comment = models.DateTimeField()
    content_comment = models.TextField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_comment} - {self.content_comment[:50]}..."
    
    class Meta:
        verbose_name = "Recomendación de libro"
        verbose_name_plural = "Recomendaciones de libros"
        ordering = ['-date_comment']
