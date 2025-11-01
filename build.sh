#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

# Измените эту строку при необходимости для вашего менеджера пакетов (pip, poetry и т.д.)
make install

# Преобразование статических файлов
make collectstatic

# Применение всех ожидающих миграций базы данных
make migrate