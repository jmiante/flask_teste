from flask import render_template, url_for, jsonify, redirect
from flask_login import login_required, login_user, logout_user, current_user

from app import app
from app.forms import FilmeForm, LoginForm, UserForm, FilmeComentarioForm
from app.models import Filmes, User

@app.route('/')
def homepage():
    context = {
        'usuario': 'Jonathas',
        'idade': 34
    }
    
    return render_template('index.html', context=context)


@app.route('/novo_usuario', methods=['GET', 'POST'])
def newUser():
    form = UserForm()
    if form.validate_on_submit():
        user = form.get_user()        
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('novo_usuario.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/api/dados')
def dados():
    dados = {"mensagem": "Dados do back-end!"}
    return jsonify(dados)


@app.route('/calcular/<int:valor>')
def calcular(valor):
    context = {
        'valor': valor,
        'valor_dobro': valor * 2
    }
    return render_template('calcular.html', context=context)


@app.route('/filmes/novo', methods=['GET', 'POST'])
@login_required
def novoFilme():
    form = FilmeForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))

    return render_template('filme_novo.html', form=form)


@app.route('/filme/lista')
def listaFilme():
    filmes = Filmes.query.order_by(Filmes.titulo.desc()).all()
    return render_template('filme_lista.html', objects=filmes)


@app.route('/filme/<int:id>', methods=['GET', 'POST'])
def detailFilme(id):    
    filme = Filmes.query.get(id)
    form = FilmeComentarioForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        form.save(filme.id, current_user.id)

    return render_template('filme_detail.html', object=filme, form=form)

