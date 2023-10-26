# Utilizar una imagen base de Python 3.10
FROM python:3.10

# Establecer variables de entorno para Python
ENV PYTHONUNBUFFERED=1

# Crear y establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos e instalar las dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente del proyecto al contenedor
COPY IntegraSoft_Front /app/IntegraSoft_Front

# Cambiar el directorio de trabajo
WORKDIR /app/IntegraSoft_Front

# Ejecutar collectstatic
RUN python manage.py collectstatic --noinput

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8001

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]


