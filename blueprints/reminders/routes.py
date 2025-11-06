from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from extensions import db
from models import Reminder

bp = Blueprint('reminders', __name__, url_prefix='/reminders')

@bp.route('/')
@login_required
def index():
    items = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.remind_at).all()
    return render_template("reminders/index.html", items=items, now=datetime.now())

@bp.route('/create', methods=['POST'])
@login_required
def create():
    title = request.form.get('title', '').strip()
    remind_at_str = request.form.get('remind_at', '').strip()
    
    if not title or not remind_at_str:
        flash('Preencha todos os campos obrigatórios.', 'danger')
        return redirect(url_for('reminders.index'))
    
    try:
        # Converter string para datetime
        remind_at = datetime.strptime(remind_at_str, '%Y-%m-%dT%H:%M')
        
        # Verificar se a data não é no passado
        if remind_at < datetime.now():
            flash('A data do lembrete não pode ser no passado.', 'warning')
            return redirect(url_for('reminders.index'))
        
        reminder = Reminder(
            title=title,
            remind_at=remind_at,
            user_id=current_user.id
        )
        db.session.add(reminder)
        db.session.commit()
        flash('Lembrete criado com sucesso!', 'success')
    except ValueError:
        flash('Data inválida. Use o formato correto.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar lembrete: {str(e)}', 'danger')
    
    return redirect(url_for('reminders.index'))

@bp.route('/toggle/<int:id>', methods=['POST'])
@login_required
def toggle(id):
    reminder = Reminder.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    reminder.done = not reminder.done
    db.session.commit()
    
    status = 'visto' if reminder.done else 'reaberto'
    flash(f'Lembrete marcado como {status}.', 'success')
    return redirect(url_for('reminders.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    reminder = Reminder.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(reminder)
    db.session.commit()
    flash('Lembrete excluído com sucesso.', 'success')
    return redirect(url_for('reminders.index'))