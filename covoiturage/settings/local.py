from .base import *

DEBUG = config('DEBUG', default=True, cast=bool)

# Local Storage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Celery Eager for easier debugging locally if needed
# CELERY_TASK_ALWAYS_EAGER = True
