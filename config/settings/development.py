from .base import *

DEBUG = True

INSTALLED_APPS += ['django_extensions']

# En desarrollo podés usar SQLite si no tenés MySQL instalado
# Descomenta las siguientes líneas y comentá el DATABASES de base.py
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
