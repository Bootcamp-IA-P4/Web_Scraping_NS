from django.shortcuts import render
from .models import BookRecommendation

def home(request):
    books = BookRecommendation.objects.all()  # O cualquier lógica para la vista
    return render(request, 'scraper/home.html', {'books': books})