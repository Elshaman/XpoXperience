from flask import Flask,render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    compras = db.relationship('Venta', backref='cliente', lazy='dynamic')

    def __repr__(self):
        return '<Cliente {}>'.format(self.username)

class Venta(db.Model):
    __tablename__ = "ventas"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))

    def __repr__(self):
        return '<Venta {}>'.format(self.id)

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), index=True, unique=True)
    precio = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    imagen = db.Column(db.String(120), index=True, nullable = False)

class DetalleVenta(db.Model):
    __tablename__ = "detalles"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'))


##from models import Cliente

@app.route('/')
def index():
    paises = ["colombia"]
    return render_template("main.html" , paises = paises)

