# Utilizar una imagen base de Python 3.10
FROM python:3.10 AS build

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

# Utilizar una imagen base de Nginx
FROM nginx:alpine

# Instalar Gunicorn
RUN apk add --no-cache py3-gunicorn

# Copiar los archivos estáticos recopilados a la imagen de Nginx
COPY --from=build /app/IntegraSoft_Front/staticfiles /static/

# Copiar la configuración de Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar el código fuente y los archivos de requisitos
COPY --from=build /app/IntegraSoft_Front /app/IntegraSoft_Front
COPY --from=build /app/requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Cambiar el directorio de trabajo
WORKDIR /app/IntegraSoft_Front

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8001

# Comando para ejecutar Gunicorn y Nginx
CMD ["sh", "-c", "gunicorn IntegraSoft_Front.wsgi:application --bind 0.0.0.0:8001 & nginx -g 'daemon off;'"]

