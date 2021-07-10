"""
Django settings for pycommerce project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!=on7gbmn5@^0#cviwi4-4ywmo5rqtym=sw35$iwm&7jxzod16'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'social_django',  # add social login app to installed apps
	'irish.apps.IrishConfig',
	'adumin.apps.AduminConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'social_django.middleware.SocialAuthExceptionMiddleware',  # exception middleware for social login
]

ROOT_URLCONF = 'pycommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # this list is empty by default. But we have this so we can have our templates in one folder instead of scattered in different applications
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

				# social django context processors
				'social_django.context_processors.backends',
				'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'pycommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# do this so you can have your static files in one static directory instead of separately in different applications
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
LOGIN_URL = 'irish:login'
LOGIN_REDIRECT_URL = 'irish:index'
LOGOUT_URL = 'irish:logout'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',  # backend for google social login
    'social_core.backends.github.GithubOAuth2',  # backend for github social login
	'social_core.backends.facebook.FacebookOAuth2',  # backend for facebook social login
	'django.contrib.auth.backends.ModelBackend',
]

# keys
SOCIAL_AUTH_GITHUB_KEY = 'b95437dff7d3d49f1ba3'
SOCIAL_AUTH_GITHUB_SECRET = '3c3209d886f2be1259289ffaa5b6168d599ed7de'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1073181510049-t6s98uk4p903iv1ee2g1i67n791oile6.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '4wo-3sZunV6x_cFD4h_a1Ckv'

SOCIAL_AUTH_FACEBOOK_KEY = '4080175278738610'
SOCIAL_AUTH_FACEBOOK_SECRET = '66ea525a98fae19373b9d08692a46082'
