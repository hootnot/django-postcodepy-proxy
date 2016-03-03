"""conftest.py - read py py.test."""
import os


def pytest_configure():
    from django.conf import settings

    settings.configure(
        SECRET_KEY='not that secret for testing purpose',
        SITE_ID=303,
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'postcodepy_proxy',
        ],
        POSTCODEPY={
           "AUTH": {
             "API_ACCESS_KEY": os.getenv("ACCESS_KEY"),
             "API_ACCESS_SECRET": os.getenv("ACCESS_SECRET"),
           },
        }
    )
