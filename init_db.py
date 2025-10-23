from biblioteca_virtual import create_app, db
from biblioteca_virtual.models import Usuario, Livro
from dotenv import load_dotenv
load_dotenv()

app = create_app()

with app.app_context():
    db.create_all()
    print('Banco de dados e tabelas criados com sucesso!')
