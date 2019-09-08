import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('WEB_SERVER_SECRET_KEY') or 'abcdef020301abc8c86f'

    DB_OPS_IP = '45.78.76.192'
    DB_OPS_PORT = '30501'
    # DB_OPS_IP = os.environ.get('DB_OPS_IP')
    # DB_OPS_PORT = os.environ.get('DB_OPS_PORT')
    DB_OPS_URL = DB_OPS_IP + ':' + DB_OPS_PORT

    DATA_CSV_PATH = './app/data_process/data.csv'
    DATA_CSV_SEND_PATH = 'data_process/data.csv'
