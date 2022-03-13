DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'comics',
        'USER': 'iskeltan'
    }
}

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

ELASTICSEARCH = {
    'url': 'http://127.0.0.1:9200',
    'index_name': 'comics',
    'number_of_shards': 1,
    'number_of_replicas': 1
}