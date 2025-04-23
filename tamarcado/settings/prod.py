from tamarcado.settings.base import * # assim conseguimos importar todos os valores que foram definidos no arquivo base.py

DEBUG = False

ALLOWED_HOSTS = ['*'] # * para definir que todos possam acessar a aplicação quando o servidor estiver em produção


DATABASES = { #utilizado databases nesse tipo de arquivo para integrar o banco de dados como postgres
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}