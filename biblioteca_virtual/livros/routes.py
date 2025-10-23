
# Importações principais do Flask e extensões
from flask import render_template, redirect, url_for, flash, request  # render_template para páginas, redirect/url_for para navegação, flash para mensagens, request para dados recebidos
from flask_login import login_required, current_user  # login_required protege rotas, current_user traz usuário logado
from . import livros_bp  # Blueprint das rotas de livros
from ..models import Livro, Usuario, Emprestimo  # Modelos principais
from .. import db  # Instância do banco de dados SQLAlchemy
from .forms import LivroForm  # Formulário de cadastro/edição de livros
from .emprestimos_forms import EmprestimoForm, DevolucaoForm  # Formulários de empréstimo e devolução


# Página principal: lista todos os livros cadastrados
# Protegida por login_required (só usuários autenticados)
@livros_bp.route('/')
@login_required
def listar_livros():
    livros = Livro.query.all()  # Busca todos os livros
    return render_template('livros.html', livros=livros)  # Renderiza template com lista


# Empréstimos

# Página de histórico de empréstimos
@livros_bp.route('/emprestimos', methods=['GET'])
@login_required
def listar_emprestimos():
    # Busca todos os empréstimos, ordenando por data mais recente
    emprestimos = Emprestimo.query.order_by(Emprestimo.data_emprestimo.desc()).all()
    return render_template('emprestimos.html', emprestimos=emprestimos)


# Página/formulário para registrar novo empréstimo
@livros_bp.route('/emprestimo/novo', methods=['GET', 'POST'])
@login_required
def novo_emprestimo():
    form = EmprestimoForm()  # Instancia formulário
    # Preenche opções de usuário e livro (só livros disponíveis)
    form.usuario.choices = [(u.id, u.username) for u in Usuario.query.all()]
    form.livro.choices = [(l.id, l.titulo) for l in Livro.query.filter_by(disponivel=True)]
    if form.validate_on_submit():  # Se o formulário for enviado e válido
        # Cria registro de empréstimo
        emprestimo = Emprestimo(
            usuario_id=form.usuario.data,
            livro_id=form.livro.data,
            data_emprestimo=form.data_emprestimo.data
        )
        livro = Livro.query.get(form.livro.data)
        livro.disponivel = False  # Marca livro como emprestado
        db.session.add(emprestimo)
        db.session.commit()  # Salva no banco
        flash('Empréstimo registrado!')  # Mensagem de sucesso
        return redirect(url_for('livros.listar_emprestimos'))
    return render_template('emprestimo_form.html', form=form)


# Página/formulário para registrar devolução de empréstimo
@livros_bp.route('/emprestimo/<int:id>/devolver', methods=['GET', 'POST'])
@login_required
def devolver_emprestimo(id):
    emprestimo = Emprestimo.query.get_or_404(id)  # Busca empréstimo pelo ID
    # Passa data do empréstimo para validação do formulário
    form = DevolucaoForm(data_emprestimo=emprestimo.data_emprestimo)
    if form.validate_on_submit():
        emprestimo.data_devolucao = form.data_devolucao.data  # Atualiza data
        emprestimo.devolvido = True  # Marca como devolvido
        livro = Livro.query.get(emprestimo.livro_id)
        livro.disponivel = True  # Torna livro disponível novamente
        db.session.commit()  # Salva alterações
        flash('Devolução registrada!')
        return redirect(url_for('livros.listar_emprestimos'))
    return render_template('devolucao_form.html', form=form, emprestimo=emprestimo)


# Página/formulário para cadastrar novo livro
@livros_bp.route('/livro/novo', methods=['GET', 'POST'])
@login_required
def novo_livro():
    form = LivroForm()  # Instancia formulário
    if form.validate_on_submit():
        # Cria novo livro com dados do formulário
        livro = Livro(
            titulo=form.titulo.data,
            autor=form.autor.data,
            ano=form.ano.data
        )
        db.session.add(livro)
        db.session.commit()  # Salva no banco
        flash('Livro cadastrado com sucesso!')
        return redirect(url_for('livros.listar_livros'))
    return render_template('livro_form.html', form=form)


# Página/formulário para editar dados de um livro
@livros_bp.route('/livro/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_livro(id):
    livro = Livro.query.get_or_404(id)  # Busca livro pelo ID
    form = LivroForm(obj=livro)  # Preenche formulário com dados atuais
    if form.validate_on_submit():
        # Atualiza dados do livro
        livro.titulo = form.titulo.data
        livro.autor = form.autor.data
        livro.ano = form.ano.data
        db.session.commit()  # Salva alterações
        flash('Livro atualizado!')
        return redirect(url_for('livros.listar_livros'))
    return render_template('livro_form.html', form=form, editar=True)


# Rota para excluir um livro
@livros_bp.route('/livro/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_livro(id):
    livro = Livro.query.get_or_404(id)  # Busca livro pelo ID
    db.session.delete(livro)  # Remove do banco
    db.session.commit()
    flash('Livro excluído!')
    return redirect(url_for('livros.listar_livros'))
