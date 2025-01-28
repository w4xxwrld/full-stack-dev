#!/bin/bash
# Скрипт для резервного копирования файлов

echo "Введите путь к файлу, который хотите скопировать:"
read FILE_PATH

if [ ! -f "$FILE_PATH" ]; then
  echo "Ошибка: Файл не существует." >&2
  exit 1
fi

BACKUP_DIR="$HOME/backup_configs_$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

cp "$FILE_PATH" "$BACKUP_DIR"

if [ $? -eq 0 ]; then
  echo "Файл успешно скопирован в $BACKUP_DIR"
else
  echo "Ошибка при копировании файла!" >&2
fi
