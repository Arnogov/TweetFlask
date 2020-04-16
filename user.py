from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(140), nullable=False)
    password = db.Column(db.String(80), nullable=True)
    
