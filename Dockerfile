# Usamos una imagen base de Python
FROM python:3.9-slim

# Instalamos dependencias del sistema para Firefox y Geckodriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    firefox-esr \
    libx11-xcb1 \
    libxtst6 \
    libxrender1 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libasound2 \
    fonts-liberation \
    libgl1-mesa-dri \
    libpci3 \
    && rm -rf /var/lib/apt/lists/*

# Instalamos Geckodriver
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.36.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.36.0-linux64.tar.gz

# Crea un directorio para los datos del perfil de Firefox
RUN mkdir -p /usr/local/share/firefox/user-data

# Establece la variable de entorno para usar un directorio único por contenedor
ENV FIREFOX_USER_DATA_DIR=/usr/local/share/firefox/user-data-${HOSTNAME}

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos necesarios al contenedor
COPY . .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Otorgamos permisos adecuados para los archivos
RUN chmod -R 777 /app

# Exponemos el puerto de la aplicación Streamlit
EXPOSE 8501

# Configuración para que Selenium use el directorio de datos de usuario
ENV MOZ_USER_DIR=$FIREFOX_USER_DATA_DIR

# Comando para iniciar la aplicación de Streamlit
CMD ["streamlit", "run", "project_webScraping/scraper/front/app.py"]
