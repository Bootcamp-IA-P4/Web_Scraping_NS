import streamlit as st
import os 
import sys
import django

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.insert(0, project_path)
# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_webScraping.settings')
django.setup()

from scraper.models import BookRecommendation
from scraper.services.book_scraper import BookScraper

st.title("Web Scraping de Comentarios de Libros")

if st.button('Iniciar Scraping'):
    with st.spinner('Iniciando scraping...'):
        scraper = BookScraper()
        try:
            scraper.setup_driver()
            total_saved = scraper.scrape_comments()
            st.success(f'Se han encontrado {total_saved} comentarios')
        finally:
            scraper.close_driver()

st.header('Comentarios guardados')
comments = BookRecommendation.objects.all().order_by('-date')

if comments:
    for comment in comments:
        with st.container():
            st.write(f"**{comment.author}**")
            st.write(f"Fecha: {comment.date}")
            st.write(f"Comentario: {comment.content}")
            st.write("---")

else:
    st.info('No hay comentarios disponibles, empieza el web scraping para obtener comentarios')
