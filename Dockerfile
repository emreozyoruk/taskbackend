FROM python:3.10-slim

# Çalışma dizinini oluştur
WORKDIR /app

# requirements.txt dosyasını kopyala ve gerekli paketleri yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamanın tüm dosyalarını kopyala
COPY . .

# Uvicorn ile FastAPI'yi başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
