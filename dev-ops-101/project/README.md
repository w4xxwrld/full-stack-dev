# Автоматизация настройки Linux-сервера

## Структура проекта
- `update_server.sh` — обновляет и апгрейдит пакеты.
- `install_nginx.sh` — устанавливает и проверяет Nginx.
- `create_user.sh` — создает пользователей и группы с вводом данных.
- `backup_configs.sh` — копирует файл в директорию с резервными копиями.
- `master_setup.sh` — запускает все скрипты по порядку.

## Инструкции по использованию
1. **Клонируйте репозиторий**:
   ```bash
   git clone <github.com/w4xxwrld/full-stack-dev/dev-ops-101/project>
   cd dev-ops-101/projects
