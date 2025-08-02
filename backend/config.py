import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://myuser:mot_de_passe@db_esme:5432/cleclat')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
