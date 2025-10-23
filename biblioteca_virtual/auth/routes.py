
# Importações principais do Flask e extensões
from flask import render_template, redirect, url_for, flash, request  # render_template para páginas, redirect/url_for para navegação, flash para mensagens, request para dados recebidos
from flask_login import login_user, logout_user, login_required  # login_user faz login, logout_user faz logout, login_required protege rotas
from . import auth_bp  # Blueprint das rotas de autenticação
from ..models import Usuario  # Modelo de usuário
from .. import db, login_manager  # Instância do banco e gerenciador de login
from .forms import LoginForm, RegisterForm  # Formulários de login e cadastro


# Função para carregar usuário logado (usada pelo Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Página/formulário de login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instancia formulário
    if form.validate_on_submit():  # Se o formulário for enviado e válido
        user = Usuario.query.filter_by(username=form.username.data).first()  # Busca usuário
        # Verifica senha usando hash
        if user and user.check_password(form.password.data):
            login_user(user)  # Faz login
            return redirect(url_for('livros.listar_livros'))  # Redireciona para livros
        flash('Usuário ou senha inválidos.')  # Mensagem de erro
    return render_template('login.html', form=form)


# Rota para logout do usuário
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Encerra sessão
    return redirect(url_for('auth.login'))


# Página/formulário de cadastro de usuário
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Instancia formulário
    if form.validate_on_submit():
        # Verifica se nome de usuário já existe
        if Usuario.query.filter_by(username=form.username.data).first():
            flash('Nome de usuário já existe.')
        else:
            user = Usuario(username=form.username.data)
            user.set_password(form.password.data)  # Gera hash seguro da senha
            db.session.add(user)
            db.session.commit()  # Salva no banco
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
