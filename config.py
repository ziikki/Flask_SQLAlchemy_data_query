import os
#import pymysql

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'what-about-dah'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                               'mysql+pymysql://root:Password@localhost/postsdb'
    #                          'sqlite:///' + os.path.join(basedir, 'app.db')

    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
