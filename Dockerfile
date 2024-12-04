# Gunakan image Python
FROM python:3.9-slim

# Set direktori kerja
WORKDIR /app

# Salin file requirements dan aplikasi ke dalam container
COPY requirements.txt ./
COPY app.py ./

# Instal dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Ekspos port yang digunakan aplikasi
EXPOSE 8501

# Perintah untuk menjalankan aplikasi Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
