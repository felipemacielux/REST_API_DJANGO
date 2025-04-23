# Quando o servidor for inicializado ele pegará essas configurações

from tamarcado.settings.base import * # assim conseguimos importar todos os valores que foram definidos no arquivo base.py

DEBUG = True

ALLOWED_HOSTS = []
LOGGING = {
    **LOGGING,
    'loggers': {
        '': {  # '' representa o logger "raíz" (root). Todos "loggers" herdarão dele.
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}