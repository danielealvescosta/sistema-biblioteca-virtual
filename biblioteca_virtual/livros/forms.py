from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class LivroForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=120)])
    autor = StringField('Autor', validators=[DataRequired(), Length(max=80)])
    ano = IntegerField('Ano', validators=[DataRequired(), NumberRange(min=1000, max=2100)])
    submit = SubmitField('Salvar')
