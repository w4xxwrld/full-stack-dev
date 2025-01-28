#!/bin/bash
# Скрипт для установки и проверки Nginx

echo "Установка Nginx..."
sudo apt install nginx -y

echo "Запуск Nginx..."
sudo systemctl start nginx
sudo systemctl enable nginx

echo "Проверка статуса Nginx..."
sudo systemctl status nginx --no-pager

if systemctl is-active --quiet nginx; then
  echo "Nginx установлен и работает корректно!"
else
  echo "Ошибка: Nginx не запустился." >&2
  exit 1
fi
