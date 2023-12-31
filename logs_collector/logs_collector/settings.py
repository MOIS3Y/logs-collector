import environ
from pathlib import Path
from datetime import timedelta

from . import __version__, __status__


# █▀█ █▀█ █▀█ ▀█▀ ▀
# █▀▄ █▄█ █▄█ ░█░ ▄
# -- -- -- -- -- --

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# █▀▀ █▄░█ █░█ ▀
# ██▄ █░▀█ ▀▄▀ ▄
# -- -- -- -- --

# Set default environ variables:
env = environ.Env(
    # set casting default value
    VERSION=(str, __version__),
    ENVIRONMENT=(str, __status__),
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'j9QGbvM9Z4otb47'),
    DATA_DIR=(Path, BASE_DIR / 'data'),
    CSRF_TRUSTED_ORIGINS=(list, []),
    ALLOWED_HOSTS=(list, ['*']),
    TZ=(str, 'UTC'),
)

# Read .env file if exist:
environ.Env.read_env(BASE_DIR / '.env')


# █▀▀ █▀█ █▀█ █▀▀ ▀
# █▄▄ █▄█ █▀▄ ██▄ ▄
# -- -- -- -- -- -

VERSION = env('VERSION')

ENVIRONMENT = env('ENVIRONMENT')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'collector.apps.CollectorConfig',  # main app
    'account.apps.AccountConfig',  # account app
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_spectacular',
    "crispy_forms",
    "crispy_bootstrap5",
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor.plugins.phonenumber',  # <- if you want phone number capability
    'two_factor',
    'django_cleanup.apps.CleanupConfig',  # required bottom
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'collector.middleware.HttpResponseNotAllowedMiddleware',
]

ROOT_URLCONF = 'logs_collector.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # default:
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # collector:
                'collector.context_processors.metadata',
                'collector.context_processors.storage_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'logs_collector.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa:E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa:E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa:E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa:E501
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TZ')

USE_I18N = True

USE_TZ = True


# █▀ ▀█▀ ▄▀█ ▀█▀ █ █▀▀ ▀
# ▄█ ░█░ █▀█ ░█░ █ █▄▄ ▄
# -- -- -- -- -- -- -- -

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Whitenoise:
# https://whitenoise.readthedocs.io/en/stable/django.html
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'


# █▀▄ ▄▀█ ▀█▀ ▄▀█ ▀
# █▄▀ █▀█ ░█░ █▀█ ▄
# -- -- -- -- -- --

# Build paths inside the project for db and storage.
DATA_DIR = env('DATA_DIR')

# Create DATA_DIR ignore if exist:
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

# Custom file storage path
MEDIA_ROOT = DATA_DIR / 'archives'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
            "base_url": "/download/archives/",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# █▀▄ ▄▀█ ▀█▀ ▄▀█ █▄▄ ▄▀█ █▀ █▀▀ ▀
# █▄▀ █▀█ ░█░ █▀█ █▄█ █▀█ ▄█ ██▄ ▄
# -- -- -- -- -- -- -- -- -- -- --

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': env.db_url(
        'DB_URL',
        default=f'sqlite:///{DATA_DIR / "db.sqlite3"}'
    )
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# █▀▀ ▀▄▀ ▀█▀ █▀▀ █▄░█ ▀█▀ █ █▀█ █▄░█ █▀ ▀
# ██▄ █░█ ░█░ ██▄ █░▀█ ░█░ █ █▄█ █░▀█ ▄█ ▄
# -- -- -- -- -- -- -- -- -- -- -- -- -- -

# django-crispy-forms and crispy-bootstrap5
# https://django-crispy-forms.readthedocs.io/en/latest/
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend', ],  # noqa:E501
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',  # noqa:E501
    # 'PAGE_SIZE': 3,
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
}

if DEBUG:
    REST_FRAMEWORK.get(
        'DEFAULT_RENDERER_CLASSES', []
    ).append('rest_framework.renderers.BrowsableAPIRenderer')
    REST_FRAMEWORK.get(
        'DEFAULT_PARSER_CLASSES', []
    ).append('rest_framework.renderers.BrowsableAPIRenderer')

# https://drf-spectacular.readthedocs.io/en/latest/readme.html
SPECTACULAR_SETTINGS = {
    'TITLE': 'Logs collector API',
    'DESCRIPTION': 'Collector of archives with log files for further analysis',
    'VERSION': VERSION,
    'SERVE_INCLUDE_SCHEMA': True,
    'SERVE_PUBLIC': False,
    "SWAGGER_UI_SETTINGS": {
        "filter": True,
    },
}

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",  # noqa:E501

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",  # noqa:E501
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",  # noqa:E501
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",  # noqa:E501
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",  # noqa:E501
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",  # noqa:E501
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",  # noqa:E501
}


# ▄▀█ █░█ ▀█▀ █░█ ▀
# █▀█ █▄█ ░█░ █▀█ ▄
# -- -- -- -- -- --

LOGIN_URL = 'two_factor:login'
LOGIN_REDIRECT_URL = 'collector:index'
LOGOUT_REDIRECT_URL = 'two_factor:login'

# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'account.User'
