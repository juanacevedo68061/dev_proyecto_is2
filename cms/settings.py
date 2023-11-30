import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-l+h5q-)9z0-gsak2r@@er_3ck3-=v8+-j@wtuu$(91&g*t-02b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_DOMAIN = '127.0.0.1'
SITE_PORT = '8000'
ALLOWED_HOSTS = [SITE_DOMAIN, 'localhost', '0.0.0.0', 'cms-is2-produccion.loca.lt']
HTTP403_PAGE = '403.html'
SITE_ID = 1
CSRF_TRUSTED_ORIGINS = ['https://*.loca.lt']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cms.team.is2@gmail.com'  # Tu dirección de correo de Gmail
EMAIL_HOST_PASSWORD = 'vseb krgh vskk zdch'  # Tu contraseña de correo de Gmail (o usa variables de entorno)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "login",
    "administracion",
    "roles",
    "publicaciones",
    "PIL",
    "kanban",
    "storages",
    "comentarios",
    "froala_editor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = "cms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
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

WSGI_APPLICATION = "cms.wsgi.application"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-ar'  # o el código de idioma adecuado para tu aplicación

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



# Configuración de Google Cloud Storage
#for media storage in the bucket
##getting credential
from google.oauth2 import service_account
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR,'credencial.json'))

## configuracion para archivos multimedia
###configuration for media file storing and reriving media file from gcloud
DEFAULT_FILE_STORAGE='cms.gcloud.GoogleCloudMediaFileStorage'
GS_PROJECT_ID = 'proyectois2-402511'
GS_BUCKET_NAME = 'proyecto_is2_bucket'
MEDIA_ROOT = "media/"
UPLOAD_ROOT = 'media/uploads/'
MEDIA_URL = 'https://storage.googleapis.com/{}/'.format(GS_BUCKET_NAME)

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = 'login.Usuario'
LOGIN_URL = 'login:inicio_sesion'  # Configura la URL de inicio de sesión
LOGIN_REDIRECT_URL = 'login:perfil'  # Configura la URL de redirección después del inicio de sesión

# Either enable sending mail messages to the console:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ENTORNO = 'produccion'

if ENTORNO == 'produccion':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'cms_bd',  # Nombre de la base de datos PostgreSQL
            'USER': 'postgres',  # Usuario PostgreSQL
            'PASSWORD': '12345',  # Contraseña PostgreSQL
            'HOST': 'db',  # Nombre del servicio de la base de datos en Docker Compose
            'PORT': '5432',  # Puerto por defecto de PostgreSQL
        }
    }

if ENTORNO == 'desarrollo':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


CSRF_TRUSTED_ORIGINS = ["http://localhost:8080","http://localhost:8000","http://localhost:80",
"http://127.0.0.1:80","http://127.0.0.1:8080","http://127.0.0.1:8000"]

