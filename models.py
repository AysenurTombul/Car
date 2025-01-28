from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # Detayları app.py'deki haliyle kopyalayabilirsiniz
