import os
BASE_DIR = os.path.dirname(__file__)
SECRET_KEY = os.environ.get("RUP_SECRET", "troque-este-segredo")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "routineup.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB uploads

# --- CONFIGURAÇÃO DE EMAIL (NOVO) ---
# Define o servidor de email. Para o Gmail, é 'smtp.gmail.com'
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
# A porta. 587 é a porta padrão para TLS.
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
# Ativa a segurança TLS (recomendado)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
# O teu email (ex: seu.email@gmail.com)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# A tua palavra-passe de email ou "App Password" do Google
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# O email que aparecerá como remetente
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
# --- FIM DA CONFIGURAÇÃO DE EMAIL ---