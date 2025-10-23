
# Importações principais do Flask e extensões
from flask import jsonify, request, abort  # jsonify para respostas JSON, request para dados recebidos, abort para erros HTTP
from .. import db  # Instância do banco de dados SQLAlchemy
from . import api_bp  # Blueprint da API
from flask_login import login_required  # Protege rotas para usuários autenticados
from ..models import Livro, Emprestimo, Usuario  # Modelos principais
from datetime import date  # Manipulação de datas


# Endpoint GET para listar todos os empréstimos
# Protegido por login_required: só usuários autenticados podem acessar
@api_bp.route('/emprestimos', methods=['GET'])
@login_required
def get_emprestimos():
    # Busca todos os empréstimos no banco
    emprestimos = Emprestimo.query.all()
    # Retorna lista de dicionários com dados relevantes
    return jsonify([
        {
            'id': e.id,
            'usuario': e.usuario.username,
            'livro': e.livro.titulo,
            'data_emprestimo': e.data_emprestimo.isoformat(),
            'data_devolucao': e.data_devolucao.isoformat() if e.data_devolucao else None,
            'devolvido': e.devolvido
        } for e in emprestimos
    ])


# Endpoint POST para criar um novo empréstimo
# Recebe JSON com usuario_id, livro_id e data_emprestimo
@api_bp.route('/emprestimos', methods=['POST'])
@login_required
def criar_emprestimo():
    data = request.get_json()  # Recebe dados do corpo da requisição
    # Validação básica dos campos obrigatórios
    if not data or not all(k in data for k in ('usuario_id', 'livro_id', 'data_emprestimo')):
        abort(400)
    livro = Livro.query.get(data['livro_id'])  # Busca o livro pelo ID
    # Só permite empréstimo se o livro estiver disponível
    if not livro or not livro.disponivel:
        abort(400, 'Livro não disponível')
    # Cria o registro de empréstimo
    emprestimo = Emprestimo(
        usuario_id=data['usuario_id'],
        livro_id=data['livro_id'],
        data_emprestimo=date.fromisoformat(data['data_emprestimo'])
    )
    livro.disponivel = False  # Marca o livro como indisponível
    db.session.add(emprestimo)
    db.session.commit()  # Salva no banco
    return jsonify({'id': emprestimo.id}), 201  # Retorna o ID do novo empréstimo


# Endpoint PUT para registrar devolução de um empréstimo
# Recebe JSON com data_devolucao
@api_bp.route('/emprestimos/<int:id>/devolucao', methods=['PUT'])
@login_required
def registrar_devolucao(id):
    emprestimo = Emprestimo.query.get_or_404(id)  # Busca o empréstimo pelo ID
    data = request.get_json()
    # Valida se a data foi enviada
    if not data or 'data_devolucao' not in data:
        abort(400)
    emprestimo.data_devolucao = date.fromisoformat(data['data_devolucao'])  # Atualiza data
    emprestimo.devolvido = True  # Marca como devolvido
    livro = Livro.query.get(emprestimo.livro_id)  # Busca o livro
    livro.disponivel = True  # Torna o livro disponível novamente
    db.session.commit()  # Salva alterações
    return jsonify({'msg': 'Devolução registrada'})
from .. import db
from . import api_bp
from flask_login import login_required


# Endpoint GET para listar todos os livros
@api_bp.route('/livros', methods=['GET'])
def get_livros():
    livros = Livro.query.all()  # Busca todos os livros
    # Retorna lista de dicionários com dados dos livros
    return jsonify([{'id': l.id, 'titulo': l.titulo, 'autor': l.autor, 'ano': l.ano, 'disponivel': l.disponivel} for l in livros])


# Endpoint GET para buscar um livro específico pelo ID
@api_bp.route('/livros/<int:id>', methods=['GET'])
def get_livro(id):
    livro = Livro.query.get_or_404(id)  # Busca o livro
    return jsonify({'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor, 'ano': livro.ano, 'disponivel': livro.disponivel})


# Endpoint POST para criar um novo livro
# Protegido por login_required
@api_bp.route('/livros', methods=['POST'])
@login_required
def criar_livro():
    data = request.get_json()  # Recebe dados do corpo da requisição
    # Validação dos campos obrigatórios
    if not data or not all(k in data for k in ('titulo', 'autor', 'ano')):
        abort(400)
    # Cria o livro
    livro = Livro(titulo=data['titulo'], autor=data['autor'], ano=data['ano'])
    db.session.add(livro)
    db.session.commit()  # Salva no banco
    return jsonify({'id': livro.id}), 201  # Retorna o ID do novo livro


# Endpoint PUT para atualizar dados de um livro
@api_bp.route('/livros/<int:id>', methods=['PUT'])
@login_required
def atualizar_livro(id):
    livro = Livro.query.get_or_404(id)  # Busca o livro
    data = request.get_json()
    if not data:
        abort(400)
    # Atualiza os campos recebidos
    livro.titulo = data.get('titulo', livro.titulo)
    livro.autor = data.get('autor', livro.autor)
    livro.ano = data.get('ano', livro.ano)
    db.session.commit()  # Salva alterações
    return jsonify({'msg': 'Livro atualizado'})


# Endpoint DELETE para remover um livro
@api_bp.route('/livros/<int:id>', methods=['DELETE'])
@login_required
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)  # Busca o livro
    db.session.delete(livro)  # Remove do banco
    db.session.commit()
    return jsonify({'msg': 'Livro excluído'})
