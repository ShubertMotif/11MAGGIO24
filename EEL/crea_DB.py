from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'DATA', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'il_tuo_valore_segreto'

db = SQLAlchemy(app)

# Importazione dei mixin necessari, se usi Flask-Login
from flask_login import UserMixin

# Definizione dei modelli
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    monero_wallet = db.Column(db.String(255), nullable=True)
    tron_wallet_address = db.Column(db.String(255), nullable=True)
    private_key_TRON = db.Column(db.String(255), nullable=True)
    transaction_list = db.Column(db.Text, nullable=True)
    photos = db.relationship('Photo', backref='user', lazy=True)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price_eur = db.Column(db.Float, nullable=True)
    price_monero = db.Column(db.Float, nullable=True)
    province = db.Column(db.String(100), nullable=True)
    monero_address = db.Column(db.String(255), nullable=True)
    tron_wallet_address = db.Column(db.String(255), nullable=True)
    categoria = db.Column(db.String(255), nullable=True)
    is_PRIVATO= db.Column(db.Boolean, nullable=False)
    is_SPEDIZIONE = db.Column(db.Boolean, nullable=False)
    costo_spedizione=db.Column(db.Float, nullable=True)

class Offerta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prezzo_monero = db.Column(db.Float, nullable=False)
    quantita_monero = db.Column(db.Float, nullable=False)
    quantita_usdt = db.Column(db.Float, nullable=False)
    indirizzo_monero_offerta = db.Column(db.String(255), nullable=False)
    indirizzo_usdt_offerta = db.Column(db.String(255), nullable=False)
    tipo_offerta = db.Column(db.String(50), nullable=False)  # 'buy' o 'sell'
    utente_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    utente = db.relationship('User', backref='offerte')
    private_key_USDT_hex=db.Column(db.String(255), nullable=True)
    bilancio_usdt= db.Column(db.Float, nullable=False)
    bilancio_xmr= db.Column(db.Float, nullable=False)
    indirizzo_BUY_USDT = db.Column(db.String(255), nullable=True)
    indirizzo_BUY_XMR = db.Column(db.String(255), nullable=True)
    XMR_name=db.Column(db.String(255), nullable=True)
    bilancio_xmr_sbloccato = db.Column(db.Float, nullable=False)
    is_FILLED = db.Column(db.Boolean, nullable=False)
    indirizzo_SELL_USDT = db.Column(db.String(255), nullable=True)
    indirizzo_SELL_XMR = db.Column(db.String(255), nullable=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

# Funzione per creare il database
def create_database():
    db.create_all()
    print("Database creato con successo!")

if __name__ == '__main__':
    with app.app_context():
        create_database()
