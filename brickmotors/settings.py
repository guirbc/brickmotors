from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url



BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "1") == "1"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".app.github.dev", ".githubpreview.dev"]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000", "http://127.0.0.1:8000",
    "https://*.app.github.dev", "https://*.githubpreview.dev",
]
forward_host = os.getenv("FORWARDED_HOST")
if forward_host:
    ALLOWED_HOSTS += [forward_host]
    CSRF_TRUSTED_ORIGINS += [f"https://{forward_host}"]

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "django_filters",
    "widget_tweaks",
    "market","payments",
    "anymail",
    "brickmotors.accounts",  # <= aqui!
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "brickmotors.urls"

TEMPLATES = [{
    "BACKEND":"django.template.backends.django.DjangoTemplates",
    "DIRS":[BASE_DIR / "templates"],
    "APP_DIRS":True,
    "OPTIONS":{"context_processors":[
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "brickmotors.wsgi.application"

# === Banco de dados: prioridade para DATABASE_URL; fallback para POSTGRES_*; senão SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Ex.: postgresql://user:pass@host:5432/dbname  (em produção use ?sslmode=require)
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,                         # pooling simples
            ssl_require=os.getenv("DB_SSL", "0")=="1"
        )
    }

elif os.getenv("POSTGRES_DB"):
    # Modo que você já usava com variáveis separadas
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        }
    }

else:
    # Dev rápido/local
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN","")
MP_PUBLIC_KEY  = os.getenv("MP_PUBLIC_KEY","")
MP_WEBHOOK_SECRET = os.getenv("MP_WEBHOOK_SECRET","dev-webhook-secret")

LOGIN_URL = "/conta/login/"
LOGIN_REDIRECT_URL = "/"     # depois de logar
LOGOUT_REDIRECT_URL = "/"    # depois de sair
# --- Autenticação / redirecionamentos ---
LOGIN_REDIRECT_URL = "market:home"      # ajuste se teu nome for diferente
LOGOUT_REDIRECT_URL = "market:home"

# Token de expiração (para o link de ativação)
PASSWORD_RESET_TIMEOUT = 60 * 60 * 24 * 3  # 3 dias

# --- E-mail ---
# Em desenvolvimento: imprime os e-mails no console
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    "BrickMotors <no-reply@brickmotors.com>"
)

# Em produção, defina via .env:
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.sendgrid.net
# EMAIL_PORT=587
# EMAIL_HOST_USER=apikey
# EMAIL_HOST_PASSWORD=xxx
# EMAIL_USE_TLS=1
# DEFAULT_FROM_EMAIL="BrickMotors <no-reply@brickmotors.com>"
# settings.py

ALLOWED_HOSTS = [
    "localhost", "127.0.0.1",
    ".app.github.dev", ".githubpreview.dev",
]

CSRF_TRUSTED_ORIGINS = [
    # local - http e https
    "http://localhost:8000", "http://127.0.0.1:8000",
    "https://localhost:8000", "https://127.0.0.1:8000",
    # Codespaces
    "https://*.app.github.dev", "https://*.githubpreview.dev",
]

forward_host = os.getenv("FORWARDED_HOST")
if forward_host:
    ALLOWED_HOSTS += [forward_host]
    CSRF_TRUSTED_ORIGINS += [f"https://{forward_host}"]

EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
ANYMAIL = {
    "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY"),
}

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Brick Motors <brickmotorssc@gmail.com>")