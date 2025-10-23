
# Importa FlaskForm para criar formulários seguros (CSRF)
from flask_wtf import FlaskForm
# Campos de formulário: seleção, data, botão
from wtforms import SelectField, DateField, SubmitField
# Validação de campos obrigatórios
from wtforms.validators import DataRequired, ValidationError

# Formulário para registrar empréstimo de livro
class EmprestimoForm(FlaskForm):
    usuario = SelectField('Usuário', coerce=int, validators=[DataRequired()])  # Seleção de usuário
    livro = SelectField('Livro', coerce=int, validators=[DataRequired()])  # Seleção de livro
    data_emprestimo = DateField('Data do Empréstimo', validators=[DataRequired()])  # Data do empréstimo
    submit = SubmitField('Registrar Empréstimo')  # Botão de envio

# Formulário para registrar devolução de livro
class DevolucaoForm(FlaskForm):
    data_devolucao = DateField('Data da Devolução', validators=[DataRequired()])  # Data da devolução
    submit = SubmitField('Registrar Devolução')  # Botão de envio

    def __init__(self, data_emprestimo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_emprestimo = data_emprestimo  # Data do empréstimo para validação

    # Validação customizada: devolução não pode ser antes do empréstimo
    def validate_data_devolucao(self, field):
        if self.data_emprestimo and field.data < self.data_emprestimo:
            # Mensagem de erro exibida no formulário
            raise ValidationError('A data de devolução não pode ser anterior à data do empréstimo.')

    def validate_data_devolucao(self, field):
        if self.data_emprestimo and field.data < self.data_emprestimo:
            raise ValidationError('A data de devolução não pode ser anterior à data do empréstimo.')
