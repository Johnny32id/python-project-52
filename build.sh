#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

# Убеждаемся, что Poetry использует правильную версию Python
# Удаляем собственный venv Poetry, который может использовать неправильную версию Python
if [ -d "/opt/render/project/poetry/venv" ]; then
    echo "Удаление venv Poetry с неправильной версией Python..."
    rm -rf /opt/render/project/poetry/venv 2>/dev/null || true
fi

# Удаляем все существующие окружения Poetry для принудительного пересоздания
if [ -d "$HOME/.cache/pypoetry/virtualenvs" ]; then
    rm -rf "$HOME/.cache/pypoetry/virtualenvs"/* 2>/dev/null || true
fi
if [ -d ".venv" ]; then
    rm -rf .venv 2>/dev/null || true
fi

# Ищем Python 3.12, установленный Render
PYTHON_312_PATH=""
if [ -d "/opt/render/project/python" ]; then
    # Ищем директорию Python 3.12.x
    PYTHON_DIR=$(find /opt/render/project/python -maxdepth 1 -type d -name "Python-3.12*" | head -1)
    if [ -n "$PYTHON_DIR" ]; then
        # Проверяем разные варианты имени исполняемого файла
        if [ -f "$PYTHON_DIR/bin/python3.12" ]; then
            PYTHON_312_PATH="$PYTHON_DIR/bin/python3.12"
        elif [ -f "$PYTHON_DIR/bin/python" ]; then
            PYTHON_312_PATH="$PYTHON_DIR/bin/python"
        fi
    fi
fi

# Запасной вариант: системный python3.12
if [ -z "$PYTHON_312_PATH" ]; then
    if command -v python3.12 &> /dev/null; then
        PYTHON_312_PATH=$(command -v python3.12)
    fi
fi

# Настраиваем Poetry для использования правильного Python
if [ -n "$PYTHON_312_PATH" ] && [ -f "$PYTHON_312_PATH" ]; then
    echo "Используется Python: $PYTHON_312_PATH"
    poetry env use "$PYTHON_312_PATH" || {
        echo "Ошибка при настройке Poetry, пробуем создать venv вручную..."
        export PATH="$PYTHON_DIR/bin:$PATH"
        poetry env use "$PYTHON_312_PATH"
    }
else
    echo "Предупреждение: Python 3.12 не найден, используется python3 по умолчанию"
    poetry env use python3
fi

# Измените эту строку при необходимости для вашего менеджера пакетов (pip, poetry и т.д.)
make install

# Преобразование статических файлов
make collectstatic

# Применение всех ожидающих миграций базы данных
make migrate