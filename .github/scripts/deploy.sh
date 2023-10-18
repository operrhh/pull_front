#!/bin/bash

# Cambiar al directorio del proyecto
cd /home/integrasoft/front/pull_front/IntegraSoft_Front

# Activar el entorno virtual
source /home/integrasoft/front/pull_front/entorno-virtual/bin/activate

# Obtener los últimos cambios del repositorio
git pull origin main

# Desactivar el entorno virtual si es necesario
deactivate

