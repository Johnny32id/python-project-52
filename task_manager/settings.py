import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# Построение путей внутри проекта: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Быстрые настройки для разработки - не подходят для production
# См. https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ: храните секретный ключ в секрете в production!
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError(
        'SECRET_KEY не установлен в переменных окружения. '
        'Установите SECRET_KEY в файле .env или переменных окружения.'
    )

# ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ: не запускайте с включенным debug в production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['webserver', 'localhost', '127.0.0.1', '0.0.0.0', 'testserver']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Определение приложений

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'task_manager',
    'task_manager.users.apps.UsersConfig',
    'task_manager.statuses.apps.StatusesConfig',
    'task_manager.tasks.apps.TasksConfig',
    'task_manager.labels.apps.LabelsConfig',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # по умолчанию rollbar 'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    "task_manager.rollbar_middleware.CustomRollbarNotifierMiddleware",
]

ROOT_URLCONF = 'task_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'task_manager.context_processors.navbar',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_manager.wsgi.application'

# База данных
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'TEST': {
            'NAME': 'db_test.sqlite3',
        },
    },
}
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'),
                                         conn_max_age=600),
    }

# Валидация паролей
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'

# Интернационализация
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Русский'),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'task_manager', 'locale'),
)

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Статические файлы (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'task_manager/static')

# Этот код для production может сломать режим разработки, поэтому проверяем
# режим DEBUG
if not DEBUG:
    # Указываем Django копировать статические файлы в путь `staticfiles`
    # (это специфично для Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Включаем бэкенд хранения WhiteNoise, который сжимает статические файлы
    # для уменьшения использования диска и переименовывает файлы с уникальными
    # именами для каждой версии для поддержки долгосрочного кэширования
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Тип поля первичного ключа по умолчанию
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'handlers': ['console', 'file']
        }
    }
}

ROLLBAR = {
    'access_token': os.getenv('ROLLBAR_ACCESS_TOKEN'),
    'environment': 'development' if DEBUG else 'production',
    'code_version': '1.0',
    'root': BASE_DIR,
}
