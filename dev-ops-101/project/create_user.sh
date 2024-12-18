#!/bin/bash
# Скрипт для создания пользователей и групп

echo "Введите имя нового пользователя:"
read USERNAME

echo "Хотите создать новую группу для пользователя? (y/n):"
read CREATE_GROUP

if [ "$CREATE_GROUP" == "y" ]; then
  echo "Введите имя новой группы:"
  read GROUPNAME
  sudo groupadd "$GROUPNAME"
  echo "Группа $GROUPNAME создана."
else
  echo "Введите существующую группу для пользователя:"
  read GROUPNAME
fi

sudo useradd -m -g "$GROUPNAME" "$USERNAME"
echo "Пользователь $USERNAME добавлен в группу $GROUPNAME."

# Добавить возможность задать пароль
echo "Введите пароль для пользователя $USERNAME:"
sudo passwd "$USERNAME"

echo "Настройка пользователя завершена."

