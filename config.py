import os

SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

# SQLALCHEMY_DATABASE_URI = 'postgres://localhost:5432/casting_agency2'

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']

ALGORITHMS = os.environ['ALGORITHMS']

API_AUDIENCE = os.environ['API_AUDIENCE']


token_cast_director = os.environ['token_cast_director']

token_cast_assistant = os.environ['token_cast_assistant']

token_executive_producer = os.environ['token_executive_producer']
