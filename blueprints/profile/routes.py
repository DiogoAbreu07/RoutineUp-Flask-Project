from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename # Para uploads seguros
import os # Para manipulação de ficheiros/pastas
from datetime import datetime
from extensions import db
from . import profile_bp

# Configurações de Upload (podem ir para config.py se preferir)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
UPLOAD_FOLDER = 'static/uploads/avatars' # Relativo à raiz da aplicação

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.get("/")
@login_required
def index():
    # Constrói URL do avatar (ou None se não existir)
    avatar_url = None
    if current_user.avatar_filename:
        avatar_url = url_for('static', filename=os.path.join('uploads/avatars', current_user.avatar_filename).replace("\\", "/"))
    return render_template("profile/index.html", user=current_user, avatar_url=avatar_url)

@profile_bp.post("/update-details")
@login_required
def update_details():
    name = (request.form.get("name") or "").strip()
    birth_date_raw = (request.form.get("birth_date") or "").strip()
    gender = (request.form.get("gender") or "").strip() or None
    file = request.files.get('avatar') # Obter ficheiro do formulário

    # --- Validações (Nome, Data, Género - como antes) ---
    if not name or len(name) < 2:
        flash("Informe um nome válido.", "error")
        return redirect(url_for("profile.index"))
    birth_date = current_user.birth_date
    if birth_date_raw:
        try: birth_date = datetime.strptime(birth_date_raw, "%Y-m-%d").date()
        except ValueError: flash("Data de nascimento inválida.", "error"); return redirect(url_for("profile.index"))
    elif current_user.birth_date is not None: birth_date = None
    valid_genders = [None, "", "feminino", "masculino", "outro"] # Adicionado ""
    if gender not in valid_genders: gender = None
    # --- Fim Validações ---

    # --- Processamento do Avatar ---
    avatar_changed = False
    if file and file.filename != '':
        if allowed_file(file.filename):
            # Criar nome de ficheiro seguro e único (user_id + extensão)
            filename = f"{current_user.id}.{file.filename.rsplit('.', 1)[1].lower()}"
            # Caminho completo para guardar
            upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            # Criar pasta se não existir
            os.makedirs(upload_path, exist_ok=True)
            filepath = os.path.join(upload_path, filename)

            # Apagar avatar antigo se existir um diferente
            if current_user.avatar_filename and current_user.avatar_filename != filename:
                 old_filepath = os.path.join(upload_path, current_user.avatar_filename)
                 if os.path.exists(old_filepath):
                     try: os.remove(old_filepath)
                     except OSError as e: print(f"Erro ao apagar avatar antigo: {e}")

            # Salvar o novo ficheiro
            try:
                file.save(filepath)
                current_user.avatar_filename = filename # Guarda SÓ o nome do ficheiro
                avatar_changed = True
            except Exception as e:
                 flash(f"Erro ao guardar a foto: {e}", "error")
                 return redirect(url_for("profile.index"))
        else:
            flash("Tipo de ficheiro de foto inválido. Use png, jpg, jpeg, gif, webp.", "error")
            return redirect(url_for("profile.index"))
    # --- Fim Processamento Avatar ---


    # Atualizar dados do utilizador
    current_user.name = name
    current_user.birth_date = birth_date
    current_user.gender = gender
    # avatar_filename já foi atualizado se houve upload bem-sucedido

    db.session.commit()
    flash("Detalhes atualizados com sucesso.", "info")
    return redirect(url_for("profile.index"))

# Rota update_password permanece igual
@profile_bp.post("/update-password")
@login_required
def update_password():
    current_password = request.form.get("current_password") or ""
    new_password = request.form.get("new_password") or ""
    confirm_password = request.form.get("confirm_password") or ""

    if not check_password_hash(current_user.password_hash, current_password):
        flash("Senha atual incorreta.", "error"); return redirect(url_for("profile.index"))
    if len(new_password) < 6:
        flash("A nova senha deve ter pelo menos 6 caracteres.", "error"); return redirect(url_for("profile.index"))
    if new_password != confirm_password:
        flash("A nova senha e a confirmação não coincidem.", "error"); return redirect(url_for("profile.index"))

    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    flash("Senha atualizada com sucesso.", "info")
    return redirect(url_for("profile.index"))