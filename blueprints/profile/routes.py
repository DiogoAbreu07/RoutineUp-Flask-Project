from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from extensions import db
from models import User

bp = Blueprint('profile', __name__, url_prefix='/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def index():
    # Construir URL do avatar
    avatar_url = None
    if current_user.avatar_filename:
        avatar_url = url_for('static', filename=f'uploads/avatars/{current_user.avatar_filename}')
    
    return render_template("profile/index.html", user=current_user, avatar_url=avatar_url)

@bp.route('/update-details', methods=['POST'])
@login_required
def update_details():
    try:
        # Atualizar informações pessoais
        name = request.form.get('name', '').strip()
        if name and len(name) >= 2:
            current_user.name = name
        
        birth_date_str = request.form.get('birth_date', '').strip()
        if birth_date_str:
            try:
                current_user.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Data de nascimento inválida.', 'warning')
        
        gender = request.form.get('gender', '').strip()
        if gender in ['', 'feminino', 'masculino', 'outro']:
            current_user.gender = gender if gender else None
        
        # Processar upload de avatar se houver
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename and allowed_file(file.filename):
                # Verificar tamanho do arquivo
                file.seek(0, os.SEEK_END)
                file_size = file.tell()
                file.seek(0)
                
                if file_size > MAX_FILE_SIZE:
                    flash('Arquivo muito grande. Tamanho máximo: 2MB.', 'warning')
                else:
                    # Gerar nome único para o arquivo
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    ext = secure_filename(file.filename).rsplit('.', 1)[1].lower()
                    filename = f"user_{current_user.id}_{timestamp}.{ext}"
                    
                    # Criar diretório se não existir
                    upload_folder = os.path.join(current_app.static_folder, 'uploads', 'avatars')
                    os.makedirs(upload_folder, exist_ok=True)
                    
                    # Remover avatar anterior se existir
                    if current_user.avatar_filename:
                        old_path = os.path.join(upload_folder, current_user.avatar_filename)
                        if os.path.exists(old_path):
                            try:
                                os.remove(old_path)
                            except Exception:
                                pass  # Ignorar erro ao deletar arquivo antigo
                    
                    # Salvar novo avatar
                    filepath = os.path.join(upload_folder, filename)
                    file.save(filepath)
                    current_user.avatar_filename = filename
                    flash('Foto de perfil atualizada!', 'success')
        
        db.session.commit()
        flash('Detalhes atualizados com sucesso!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar perfil: {str(e)}', 'danger')
    
    return redirect(url_for('profile.index'))

@bp.route('/update-password', methods=['POST'])
@login_required
def update_password():
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Validações
    if not current_password or not new_password or not confirm_password:
        flash('Preencha todos os campos de senha.', 'danger')
        return redirect(url_for('profile.index'))
    
    if not check_password_hash(current_user.password, current_password):
        flash('Senha atual incorreta.', 'danger')
        return redirect(url_for('profile.index'))
    
    if len(new_password) < 6:
        flash('A nova senha deve ter pelo menos 6 caracteres.', 'danger')
        return redirect(url_for('profile.index'))
    
    if new_password != confirm_password:
        flash('As senhas não coincidem.', 'danger')
        return redirect(url_for('profile.index'))
    
    try:
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Senha alterada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao alterar senha: {str(e)}', 'danger')
    
    return redirect(url_for('profile.index'))