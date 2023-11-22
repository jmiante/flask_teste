from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
import os
from werkzeug.utils import secure_filename

from app import db, bcrypt, app
from app.models import Filmes, User, FilmeComentario


class LoginForm(FlaskForm):    
    username = StringField('Username', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

    def login(self):
        user =  User.query.filter_by(username=self.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, self.senha.data):
                return user
            else:
                raise Exception('Senha Incorreta')
        else:
            raise Exception('Usuário não encontrado')


class UserForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    senha_confirmacao = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Salvar')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Username já utilizado, favor utilize outro!!!')
        
    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data)
        user = User(
            email = self.email.data,
            username = self.username.data,
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            password = senha,
        )
        db.session.add(user)
        db.session.commit()
    
    def get_user(self):
        self.save()
        return User.query.filter_by(username=self.username.data).first()


class FilmeForm(FlaskForm):
    titulo = StringField('Titulo', validators=[DataRequired()])
    ano = StringField('Ano', validators=[DataRequired()])
    resumo = TextAreaField('Resumo', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def validate_titulo(self, titulo):
        if Filmes.query.filter_by(titulo=titulo.data).first():
            raise ValidationError('Este Filme já foi incluso!!!')
    
    def save(self):
        arquivo = self.imagem.data
        nome_seguro = secure_filename(arquivo.filename)
        caminho = os.path.join(
                os.path.abspath(os.path.dirname(__file__)), # Recupera o caminho absoluto onde o arquivo routes.py está armazenado
                app.config['UPLOAD_FOLDER'], # Define a pasta de Upload que criamos
                'filmes', # define a pasta de Filmes que criamos para organizar nossos arquivos
                nome_seguro # define o nome seguro para o caminho
            )
        filme = Filmes(
            titulo = self.titulo.data,
            ano = self.ano.data,
            resumo = self.resumo.data,
            imagem=nome_seguro
        )
        arquivo.save(caminho)        
        db.session.add(filme)
        db.session.commit()


class FilmeComentarioForm(FlaskForm):
    comentario = TextAreaField('Comentário', validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def save(self, id_filme, id_user):
        comentario = FilmeComentario(
            comentario = self.comentario.data,
            id_filme = id_filme,
            id_user = id_user
        )

        db.session.add(comentario)
        db.session.commit()



