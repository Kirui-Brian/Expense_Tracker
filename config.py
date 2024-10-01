import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql://username:password@localhost/expense_tracker'
    SQLALCHEMY_TRACK_MODIFICATION = False