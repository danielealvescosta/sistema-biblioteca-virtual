from flask_wtf import FlaskForm  # Formulários seguros com CSRF
from wtforms import StringField, PasswordField, SubmitField  # Campos de formulário
from wtforms.validators import DataRequired, Length  # Validação de campos

# Formulário de login
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=80)])  # Campo de usuário
    password = PasswordField('Senha', validators=[DataRequired()])  # Campo de senha
    submit = SubmitField('Entrar')  # Botão de envio

# Formulário de cadastro
class RegisterForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=80)])  # Campo de usuário
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])  # Campo de senha (mínimo 6)
    submit = SubmitField('Cadastrar')  # Botão de envio
