from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    nome = db.Column(db.String(100))
    sobrenome = db.Column(db.String(100))
    password = db.Column(db.String(100))
    comentarios_filmes = db.relationship("FilmeComentario", backref='user', lazy=True)


class Filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    titulo = db.Column(db.String, nullable=True)
    ano = db.Column(db.Integer, nullable=True)
    resumo = db.Column(db.String, nullable=True)
    comentarios = db.relationship("FilmeComentario", backref='filme', lazy=True)
    imagem = db.Column(db.String, default='default.png')


class FilmeComentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    comentario = db.Column(db.String, nullable=True)    
    id_filme = db.Column(db.Integer, db.ForeignKey('filmes.id'), nullable=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


