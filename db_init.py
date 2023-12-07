from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

if not os.path.exists(SQLALCHEMY_DATABASE_URI):
    db.create_all()