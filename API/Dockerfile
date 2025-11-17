# 1. Imagen base de Python
FROM python:3.10

# 2. Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar dependencias
COPY requirements.txt .

# 4. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del proyecto
COPY . .

# 6. Exponer el puerto (Flask usa 5000 por defecto)
EXPOSE 5000

# 7. Comando para ejecutar la API
CMD ["python", "api.py"]
