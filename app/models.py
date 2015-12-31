from peewee import *
import os
import urllib.parse

if 'LOCAL_DEV' in os.environ:
    database = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': 'BEATTHECURVE',
        'user': os.environ['PG_USERNAME'],
        'password': '',
        'host': '127.0.0.1',
        'port': '5432',
    }
else:
    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ['DATABASE_URL'])

    database = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': url.path[1:],
        'user': url.username,
        'password': url.password,
        'host': url.hostname,
        'port': url.port,
    }

DATABASE = PostgresqlDatabase(database['name'], user=database['user'], password=database['password'],
                              host=database['host'], port=database['port'],autorollback=True)
