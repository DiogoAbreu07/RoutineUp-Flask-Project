from flask import Blueprint

# Define o Blueprint para o perfil
profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile", # URL base para esta secção
    template_folder="../../templates" # Aponta para a pasta principal de templates
)

# Importa as rotas deste blueprint
from . import routes # noqa: F401, E402