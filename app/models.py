from app import db
from datetime import datetime

class Auto (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(128))
    description = db.Column(db.String(128))
    price = db.Column(db.Float)
    transmission = db.Column(db.Boolean, default = True)
    img_url1 = db.Column(db.String(128))
    img_url2 = db.Column(db.String(128))
    img_url3 = db.Column(db.String(128)) 
    img_url4 = db.Column(db.String(128))
    status = db.Column(db.Boolean, default = True)

class Jornal(db.Model):
    rent_id = db.Column(db.Integer, primary_key = True)
    auto_id = db.Column(db.Integer, db.ForeignKey('auto.id'))
    rent_start = db.Column(db.DateTime, default = datetime.now)
    rent_end = db.Column(db.DateTime)
    cost = db.Column(db.Float)
