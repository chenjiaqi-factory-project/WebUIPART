import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('WEB_SERVER_SECRET_KEY') or 'abcdef020301abc8c86f'

    DB_OPS_IP = "127.0.0.1"
    DB_OPS_PORT = "4999"
    DB_OPS_URL = DB_OPS_IP + ':' + DB_OPS_PORT
