# Utilizar una imagen oficial de Python ligera
FROM python:3.14-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Evitar la generación de archivos pyc y habilitar salida no bufferizada
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar las dependencias sin guardar caché para reducir el tamaño de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto al contenedor
COPY . .

# Exponer el puerto 5000 (el mismo que usa Flask)
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]