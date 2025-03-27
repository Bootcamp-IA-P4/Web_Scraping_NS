# 🚀 Project Web Scraping - Comentarios de Libros 📚

## Índice

1.  [Descripción del Proyecto](#descripción-del-proyecto)
2.  [Estructura del Proyecto](#estructura-del-proyecto)
3.  [🛠️ Requisitos](#requisitos)
4.  [⚙️ Instalación](#instalación)
5.  [🕹️ Uso](#uso)
6.  [🧪 Testing](#Testing)
7.  [🐳 Despliegue con Docker](#despliegue-con-docker)
8.  [➡️ Próximos Pasos](#próximos-pasos)
9.  [🤝 Contribución](#contribución)
10. [👩‍💻 Autora](#Autora)


## Descripción del Proyecto

Este proyecto realiza web scraping de comentarios de libros de una web de recomedación de libros utilizando Selenium y Django. Los datos extraídos se almacenan en una base de datos MongoDB Atlas y se visualizan a través de una interfaz interactiva creada con Streamlit.

## Estructura del Proyecto
* project_webScraping/
    * .webscraper.log
    * db.sqlite3
    * Dockerfile
    * docker-compose.yml
    * manage.py
    * project_webScraping/
        * settings.py
        * urls.py
    * scraper/
        * models.py
        * tests.py
        * front/
            * app.py
        * migrations/
        * services/
            * book_scraper.py* project_webScraping/

    
## 🛠️ Requisitos

* Python 3.8+
* Django
* Selenium
* Streamlit
* MongoDB Atlas
* ChromeDriver
* Docker

## ⚙️ Instalación

1.  Clonar el repositorio:

    ```bash
    git clone https://github.com/Bootcamp-IA-P4/Web_Scraping_NS.git
    cd project_webScraping
    ```

2.  Crear y activar un entorno virtual:

    ```bash
    python -m venv .venv
    source .venv\Scripts\activate  # En Windows
    ```

3.  Instalar dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4.  Configurar Django:

    * Asegurar que `settings.py` esté configurado con la conexión a MongoDB Atlas.
    * Ejecutar las migraciones:

        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```

5.  Ejecutar el proyecto:

    * Ejecutar la aplicación Streamlit a la altura de manage.py:

        ```bash
        streamlit run scrape/front/app.py
        ```

## 🕹️ Uso

1.  Se abre la web con los comentarios anteriores y el scraper se ejecuta al pulsar en iniciar y guarda los comentarios en MongoDB Atlas.

## 🧪 Testing

Incluye testing:

Para probar los tests:

1. Activar el entorno virtual.
2. Ejecutar el siguiente comando:

    ```bash
    python manage.py test
    ```
<div align="center">
  <img src="https://res.cloudinary.com/artevivo/image/upload/v1742771260/Captura_de_pantalla_2025-03-24_000718_fc4zwc.png" width="700" alt="Art Brushes" />
</div>

## 🐳 Despliegue con Docker

Este proyecto puede ser fácilmente desplegado utilizando Docker Compose.

1.  **Archivo `Dockerfile` y `docker-compose.yml`:** Ya existen los archivos `Dockerfile` y `docker-compose.yml` en la raíz del proyecto. Estos archivos contienen la configuración necesaria para construir y orquestar los contenedores de la aplicación.

2.  **Levantar la aplicación con Docker Compose:**

    Para construir la imagen e iniciar los contenedores definidos en `docker-compose.yml`, ejecuta el siguiente comando en la raíz del proyecto:

    ```bash
    docker-compose up --build 
    ```

    La aplicación estará accesible en  `http://localhost:8501` para Streamlit.

    Para ver los logs de los contenedores:

    Para detener los contenedores:

    ```bash
    docker-compose down
    ```



## ➡️ Próximos Pasos

* Implementar autenticación de usuario.
* Añadir más filtros y opciones de búsqueda en la interfaz de Streamlit.
* Optimizar el rendimiento del scraper.


## 🤝 Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1.  Haz un fork del repositorio.
2.  Crea una rama con tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3.  Realiza los cambios y commitea (`git commit -am 'Añade nueva funcionalidad'`).
4.  Sube los cambios a tu rama (`git push origin feature/nueva-funcionalidad`).
5.  Abre un pull request.

## 👩‍💻 Autora

*   [Nhoeli Salazar](https://github.com/Nho89)
