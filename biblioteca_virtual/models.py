
# Importa instância do banco de dados
from . import db
# UserMixin facilita integração do modelo Usuario com Flask-Login
from flask_login import UserMixin
# Funções para hash e verificação de senha
from werkzeug.security import generate_password_hash, check_password_hash


# Modelo de usuário do sistema
# UserMixin adiciona métodos para autenticação
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nome de usuário único
    password_hash = db.Column(db.String(128), nullable=False)  # Senha armazenada como hash

    def set_password(self, password):
        # Gera hash seguro da senha
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Verifica se a senha corresponde ao hash
        return check_password_hash(self.password_hash, password)



# Modelo de livro
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    titulo = db.Column(db.String(120), nullable=False)  # Título do livro
    autor = db.Column(db.String(80), nullable=False)  # Autor
    ano = db.Column(db.Integer, nullable=False)  # Ano de publicação
    disponivel = db.Column(db.Boolean, default=True)  # Status de disponibilidade


# Modelo de empréstimo
class Emprestimo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # FK para usuário
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)  # FK para livro
    data_emprestimo = db.Column(db.Date, nullable=False)  # Data do empréstimo
    data_devolucao = db.Column(db.Date, nullable=True)  # Data da devolução
    devolvido = db.Column(db.Boolean, default=False)  # Status de devolução

    # Relacionamentos para facilitar consultas
    usuario = db.relationship('Usuario', backref='emprestimos')
    livro = db.relationship('Livro', backref='emprestimos')
