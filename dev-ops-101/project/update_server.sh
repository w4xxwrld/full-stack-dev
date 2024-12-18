#!/bin/bash
# Скрипт для обновления и апгрейда пакетов на Linux-сервере

echo "Обновление и апгрейд пакетов..."
sudo apt update && sudo apt upgrade -y

if [ $? -eq 0 ]; then
  echo "Обновление выполнено успешно!"
else
  echo "Ошибка при обновлении пакетов!" >&2
  exit 1
fi
