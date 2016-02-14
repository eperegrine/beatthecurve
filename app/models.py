from peewee import *
import os
import urllib.parse
from enum import Enum
import redis
from datetime import datetime

if 'LOCAL_DEV' in os.environ:
    database = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': 'BEATTHECURVE',
        'user': os.environ['PG_USERNAME'],
        'password': os.environ['PG_PASSWORD'],
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


DATABASE = PostgresqlDatabase(
    database=database['name'],
    user=database['user'],
    password=database['password'],
    host=database['host'],
    port=database['port'],
    autorollback=True,
    threadlocals=True)


class Semester(Enum):
    """Enum matching semester names to their integer values"""
    winter = 1
    fall = 2
    spring = 3
    summer = 4

    @classmethod
    def current_semester(cls):
        month = datetime.now().month
        if month < 3 or month == 12:
            semester = cls.winter
        elif month < 6:
            semester = cls.spring
        elif month < 9:
            semester = cls.summer
        else:
            semester = cls.fall
        return semester


class KarmaPoints(Enum):
    """Enum linking actions to the amount of KarmaPoints that should be recieved."""
    note_vote = 1
    exam_vote = 1
    upload_note = 10
    upload_exam = 10
    post_question = 3
    reply_to_question = 5


r = redis.from_url(os.environ.get("REDIS_URL"))
