#!/bin/bash
# Мастер-скрипт для автоматизации настройки сервера

echo "=== Автоматизация настройки Linux-сервера ==="

echo "1. Обновление сервера..."
bash update_server.sh || exit 1

echo "2. Установка Nginx..."
bash install_nginx.sh || exit 1

echo "3. Создание пользователей и групп..."
bash create_user.sh || exit 1

echo "4. Резервное копирование файлов..."
bash backup_configs.sh || exit 1

echo "=== Настройка завершена успешно! ==="
