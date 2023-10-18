#!/bin/bash

# Ejecutar comandos en el servidor remoto
ssh -o StrictHostKeyChecking=no $SERVER_USERNAME@$SERVER_IP << 'ENDSSH'
  cd /home/integrasoft/front/pull_front/IntegraSoft_Front
  git pull origin main
ENDSSH

