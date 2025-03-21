# Usamos una imagen base de Python
FROM python:3.9-slim

# Instalamos dependencias del sistema para Firefox y Geckodriver
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    curl \
    unzip \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Instalamos Geckodriver
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.30.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.30.0-linux64.tar.gz

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos necesarios al contenedor
COPY . .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto de la aplicación Streamlit
EXPOSE 8501

# Comando para iniciar la aplicación de Streamlit
CMD ["streamlit", "run", "project_webScraping/scraper/front/app.py"]
