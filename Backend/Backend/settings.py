import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

import rest_framework


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MODE = os.environ.get("MODE", "dev")

load_dotenv(BASE_DIR / f"{MODE}.env")
load_dotenv(BASE_DIR / "auth.env")

### Choose host

NETWORK_PROTOCOL = os.environ.get("NETWORK_PROTOCOL")
BACKEND_HOST = os.environ.get("BACKEND_HOST")
BACKEND_BASE_URL = f"{NETWORK_PROTOCOL}://{BACKEND_HOST}"
FRONTEND_HOST = os.environ.get("FRONTEND_HOST")
FRONTEND_BASE_URL = f"{NETWORK_PROTOCOL}://{FRONTEND_HOST}"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = eval(os.environ.get("DEBUG"))

ALLOWED_HOSTS = [
    "*",  # TODO: remove
    "127.0.0.1",
    "localhost",
    # TODO: add VM IP
]

# TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
# TEST_OUTPUT_DIR = 'junit-output'

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",  # TODO: remove
    "drf_spectacular",
    "corsheaders",  # TODO
    # Local applications
    "users",
    "custom_auth",
    "posts",
    "comments",
]

REMOVE_SLASH = True
APPEND_SLASH = True
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # TODO: remove or write own ???
    # "custom_auth.authentication.CookieAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        ### https://github.com/dobarkod/django-queryinspect
        # 'qinspect.middleware.QueryInspectMiddleware', ### pip install django-queryinspect
        *MIDDLEWARE,
    ]

    INTERNAL_IPS = [  # TODO
        "127.0.0.1",
    ]

ROOT_URLCONF = "Backend.urls"

# TODO: remove ???
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # required by django-debug-toolbar
        "DIRS": [],
        "APP_DIRS": True,  # required by django-debug-toolbar
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

WSGI_APPLICATION = "Backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# TODO: postgres

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "liveshare.db.sqlite3",
    }
}

# DATABASES = {
#     'default': {
#         # TODO: remove sqlite3
#         'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': os.environ.get('DB_PORT'),
#         'NAME': os.environ.get('DB_NAME', 'db.sqlite3.liveshare'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASS'),
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# TODO: remove ???

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

### OAuth

GOOGLE_OAUTH2_CLIENT_ID = os.environ.get("GOOGLE_OAUTH2_CLIENT_ID")
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH2_CLIENT_SECRET")
GOOGLE_OAUTH2_CALLBACK_PATH = os.environ.get("GOOGLE_OAUTH2_CALLBACK_PATH")

AUTH_REDIRECT_FRONTEND_PATH = os.environ.get("AUTH_REDIRECT_FRONTEND_PATH")
AUTH_REDIRECT_FRONTEND_URL = (
    f"{FRONTEND_BASE_URL}/{AUTH_REDIRECT_FRONTEND_PATH}"
)

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.environ.get("TIME_ZONE")

USE_I18N = True
# USE_L10N = True # TODO: what is it ?
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Is used by django-debug-toolbar
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_EMAIL_REQUIRED = True

################################################################################

### TODO

# SWAGGER_SETTINGS = {
#     'LOGIN_URL': '/api/accounts/login',
#     'LOGOUT_URL': '/api/accounts/logout',
#     'DEFAULT_AUTO_SCHEMA_CLASS': 'automation_homework.apricot_swagger_schema.ApricotSwaggerAutoSchema',
# }

################################################################################

# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    # TODO: add dev and prod
    FRONTEND_BASE_URL,
    # TODO: add VM IP
]

CSRF_TRUSTED_ORIGINS = [
    FRONTEND_BASE_URL,
]

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#     ),
#     'NON_FIELD_ERRORS_KEY': 'global',
#     'DEFAULT_RENDERER_CLASSES': (
#         'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
#         'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
#     ),
#     'DEFAULT_PARSER_CLASSES': (
#         'djangorestframework_camel_case.parser.CamelCaseFormParser',
#         'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
#         'djangorestframework_camel_case.parser.CamelCaseJSONParser',
#     ),
# }

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "custom_auth.authentication.CookieJWTAuthentication",
    ),
    # TODO: uncomment after creating auth
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Is used as fallback in serializers.DateTimeField()
    "DATETIME_INPUT_FORMATS": [rest_framework.ISO_8601],
    "DATETIME_FORMATS": [rest_framework.ISO_8601],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    # More configs: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
    "AUTH_ACCESS_TOKEN": "liveshare_access_token",
    "AUTH_REFRESH_TOKEN": "liveshare_refresh_token",
    "AUTH_COOKIE_DOMAIN": None,  # TODO: A string like "example.com", or None for standard domain cookie.
    "AUTH_COOKIE_SECURE": False,  # TODO: enable for prod
    "AUTH_COOKIE_HTTP_ONLY": True,  # Protection from XSS
    # Protection from CSRF (works only on modern browsers)
    "AUTH_COOKIE_SAMESITE": "Strict",
    "AUTH_COOKIE_PATH": "/",  # TODO: The path of the auth cookie.
    ### Predefined JWT claims.
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#rotate-refresh-tokens
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    # 'UPDATE_LAST_LOGIN': False,
}

# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": True,
        "defaultModelsExpandDepth": -1,  # hide models
        "defaultModelExpandDepth": 4,
    }
}
