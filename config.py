import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('WEB_SERVER_SECRET_KEY') or 'abcdef020301abc8c86f'

    # Identifiers when generating CAPTCHA
    IDENTIFIERS = 'ABCDEFGHIJKLMNPQRSTUVWXYZ12345789'

    DB_OPS_IP = '127.0.0.1'
    DB_OPS_PORT = '5000'
    # DB_OPS_IP = os.environ.get('DB_OPS_IP')
    # DB_OPS_PORT = os.environ.get('DB_OPS_PORT')
    DB_OPS_URL = DB_OPS_IP + ':' + DB_OPS_PORT

    # for account info handling api
    ACCOUNT_SERVICE_IP = os.environ.get('LOGIN_REGISTER_PART_SERVICE_HOST')
    ACCOUNT_SERVICE_PORT = os.environ.get('LOGIN_REGISTER_PART_SERVICE_PORT')
    ACCOUNT_SERVICE_URL = ACCOUNT_SERVICE_IP + ':' + ACCOUNT_SERVICE_PORT

    # for captcha supporting api
    CAPTCHA_SERVICE_IP = os.environ.get('CAPTCHA_PART_SERVICE_HOST')
    CAPTCHA_SERVICE_PORT = os.environ.get('CAPTCHA_PART_SERVICE_PORT')
    CAPTCHA_SERVICE_URL = CAPTCHA_SERVICE_IP + ':' + CAPTCHA_SERVICE_PORT

    DATA_CSV_PATH = './app/data_process/data.csv'
    DATA_CSV_SEND_PATH = 'data_process/data.csv'
