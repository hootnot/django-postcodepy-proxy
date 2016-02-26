"""
Django settings for pcp project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import postcodepy_proxy.views
import postcodepy_proxy.signalapi

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

SECRET_KEY = 'y8851u^3&i4kp^&38n7o0^_cc4t3lu8ed0j$7ie=x7%=#v8n4&'

# SECURITY WARNING: don't run with debug turned on in production!
SITE_ID = 303
DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'postcodepy_proxy',
]

