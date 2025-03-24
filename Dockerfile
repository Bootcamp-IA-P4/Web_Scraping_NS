FROM python:3.9-slim

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

RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.36.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.36.0-linux64.tar.gz

RUN mkdir -p /tmp/firefox-user-data

ENV FIREFOX_USER_DATA_DIR=/tmp/firefox-user-data-${HOSTNAME}

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 777 /app

EXPOSE 8501

ENV MOZ_USER_DIR=$FIREFOX_USER_DATA_DIR

CMD ["streamlit", "run", "project_webScraping/scraper/front/app.py"]