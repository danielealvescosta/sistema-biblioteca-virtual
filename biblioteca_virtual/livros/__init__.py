from flask import Blueprint

livros_bp = Blueprint('livros', __name__)

from . import routes
