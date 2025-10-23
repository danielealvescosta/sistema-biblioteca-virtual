# Biblioteca Virtual

Sistema web completo para cadastro de usuários, livros, empréstimos e devoluções, com autenticação, API RESTful e boas práticas de segurança.

## Funcionalidades
- Cadastro e login de usuários
- CRUD de livros
- Empréstimo e devolução de livros
- API RESTful para livros e empréstimos
- Proteção CSRF e validação de dados
- Organização em Blueprints
- Uso de variáveis de ambiente

## Tecnologias
- Python
- Flask, Flask-Login, Flask-WTF, Flask-SQLAlchemy
- SQLite

## Instalação
1. Clone o repositório e acesse a pasta do projeto.
2. Crie e ative um ambiente virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows

3. Instale as dependências:
   
   pip install -r requirements.txt
   
4. Configure o arquivo `.env`:
   ```
   SECRET_KEY=minha_chave_secreta
   DATABASE_URL=sqlite:///biblioteca.db


5. Inicialize o banco de dados:
   ```
   python init_db.py
   ```
6. Rode o sistema:
   ```
   python run.py
   ```
7. Acesse em [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Endpoints RESTful
- `/api/livros` (GET, POST)
- `/api/livros/<id>` (GET, PUT, DELETE)
- `/api/emprestimos` (GET, POST)
- `/api/emprestimos/<id>/devolucao` (PUT)

## Segurança
- Senhas com hash (Werkzeug)
- CSRF em todos os formulários (Flask-WTF)
- Variáveis sensíveis no `.env`

## Organização
- Blueprints: auth, livros, api
- Modelos: Usuario, Livro, Emprestimo

## Screenshots
Adicione aqui prints das principais telas do sistema (login, livros, empréstimos, devolução, API via Postman, etc).

## Observações
- Para usar MySQL/PostgreSQL, configure o banco e ajuste o `DATABASE_URL`.
- O sistema está pronto para produção, mas recomenda-se usar um servidor WSGI (ex: Gunicorn) e HTTPS.

---

Desenvolvido para IFSP - DevWeb3
