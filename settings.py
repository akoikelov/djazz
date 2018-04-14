"""
Django settings for test_app project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from params import DROPBOX_ACCESS_TOKEN_VALUE

INSTALLED_APPS = (
    'akoikelov.djazz',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sqlite3',
    }
}

SECRET_KEY = "secret_key_for_testing"
DROPBOX_ACCESS_TOKEN = DROPBOX_ACCESS_TOKEN_VALUE