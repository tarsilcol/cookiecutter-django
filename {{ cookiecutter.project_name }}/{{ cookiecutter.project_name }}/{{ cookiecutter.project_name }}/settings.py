# type: ignore
import datetime  # noqa: F403,F401
import os  # noqa: F403,F401
import sys  # noqa: F403,F401
from datetime import timedelta  # noqa: F403,F401

from .channel_layers import *  # noqa: F403,F401
from .databases import *  # noqa: F403,F401
from .general.caches import *  # noqa: F403,F401
from .general.settings import *  # noqa: F403,F401
from .third_parties.blacklist_domains import *  # noqa: F403,F401

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
os.path.basename(os.path.dirname(SITE_ROOT))
DJANGOENV = None

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(SITE_ROOT, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# IMPORTANT!:
# You must keep this secret, you can store it in an
# environment variable and set it with:
# export SECRET_KEY="secret-export!key-781"
# https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/#secret-key
SECRET_KEY = "secret_change_this_after"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
SITE_ID = 1

BASE_INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    'lib.common',
    'statici18n',
    'rest_framework',
    'rest_framework_simplejwt',
    'channels',
    'guardian',
    'django_dramatiq',
    'django_apscheduler',
    'corsheaders',
]

INSTALLED_APPS = [
    'accounts',
    'core',
] + BASE_INSTALLED_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
    "lib.{{ cookiecutter.project_name }}.backends.EmailBackend"
)

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        'rest_framework.parsers.MultiPartParser'
    ),
    "DEFAULT_PAGINATION_CLASS": "lib.{{ cookiecutter.project_name }}.rest.paginator.NumberDetailPagination",
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "PAGE_SIZE": 20,
}


ROOT_URLCONF = '{{ cookiecutter.project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SITE_ROOT, 'templates'),
            os.path.join(SITE_ROOT, 'static'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',

            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': DEBUG,
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICI18N_ROOT = os.path.join(SITE_ROOT, 'static')

STATICFILES_DIRS = [
    STATICI18N_ROOT
]

# STATIC DECLARATIONS ALSO FOR NGINX
STATIC_ROOT = '/resources/{{ cookiecutter.project_name }}-static/'
STATIC_URL = '/static/'
MEDIA_ROOT = '/resources/{{ cookiecutter.project_name }}-media/'
MEDIA_URL = '/media/'

LOCALE_PATHS = [os.path.join(SITE_ROOT, 'locale')]

WSGI_APPLICATION = '{{ cookiecutter.project_name }}.wsgi.application'

ASGI_APPLICATION = "{{ cookiecutter.project_name }}.routing.application"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    'lib.{{ cookiecutter.project_name }}.auth.hashers.CustomPBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    # 'django.contrib.auth.hashers.Argon2PasswordHasher',
    # 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
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


# Internationalization
# https://docs.djangoproject.com/en/1.11.4/topics/i18n/

LANGUAGE_CODE = 'en-us'

INTERNAL_IPS = ('127.0.0.1', '192.168.56.1', '10.0.2.2',)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#
# SSL CONFIGURATIONS
#

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 8640000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = "DENY"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


# Pull slug max_length out ot
SLUG_MAX_LENGTH = 64

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# DRAMATIQ SETTINGS
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": 'amqp://rabbit_user:rabbit_user_default_pass@rabbitmq:5672/',
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ]
}

# Defines which database should be used to persist Task objects when the
# AdminMiddleware is enabled.  The default value is "default".
DRAMATIQ_TASKS_DATABASE = "default"

DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKEND_OPTIONS": {"url": "redis://redis:6379"},
    "MIDDLEWARE_OPTIONS": {"result_ttl": 60000},
}

DRAMATIQ_IGNORED_MODULES = ()

DRAMATIQ_PRIORITY = {
    'high': 0,
    'medium': 50,
    'low': 100
}

DRAMATIQ_QUEUES = {
    'default': 'default',
}

# DJANGO APSCHEDULER
# More info: https://github.com/jarekwg/django-apscheduler
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

SCHEDULER_CONFIG = {
    "apscheduler.jobstores.default": {"class": "django_apscheduler.jobstores:DjangoJobStore"},
    "apscheduler.executors.processpool": {"type": "threadpool"},
}

DJANGO_NOTIFICATIONS_CONFIG = {"USE_JSONFIELD": True}

# CORS
CORS_ALLOWED_ORIGINS = []

# JWT
SIMPLE_JWT_SIGNING_KEY = "b=72^ado*%1(v3r7rga9ch)03xr=d*f)lroz94kosf!61((9=i"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=200),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=200),
}

CORS_ALLOWED_ORIGINS = []

ANONYMOUS_USER_NAME = None
