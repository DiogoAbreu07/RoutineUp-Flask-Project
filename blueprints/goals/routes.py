from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Goal

bp = Blueprint('goals', __name__, url_prefix='/goals')

@bp.route('/')
@login_required
def index():
   items = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).all()


   items_dict = []
   for goal in items:
        items_dict.append({
            'id': goal.id,
            'title': goal.title,
            'target_value': goal.target_value,
            'current_value': goal.current_value,
            'unit': goal.unit,
            'progress': goal.progress,
            'created_at': goal.created_at.isoformat() if goal.created_at else None
         })
    
   return render_template("goals/index.html", items=items_dict)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    title = request.form.get('title', '').strip()
    target_value = request.form.get('target_value', '').strip()
    unit = request.form.get('unit', '').strip()
    current_value = request.form.get('current_value', '0').strip()
    
    if not title or not target_value:
        flash('Preencha o título e o valor da meta.', 'danger')
        return redirect(url_for('goals.index'))
    
    try:
        target = float(target_value)
        current = float(current_value) if current_value else 0
        
        if target <= 0:
            flash('O valor da meta deve ser maior que zero.', 'danger')
            return redirect(url_for('goals.index'))
        
        goal = Goal(
            title=title,
            target_value=target,
            current_value=current,
            unit=unit if unit else '',
            user_id=current_user.id
        )
        goal.update_progress()  # Calcula porcentagem
        
        db.session.add(goal)
        db.session.commit()
        flash('Meta criada com sucesso!', 'success')
    except ValueError:
        flash('Valores inválidos. Use apenas números.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao criar meta: {str(e)}', 'danger')
    
    return redirect(url_for('goals.index'))

@bp.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Atualizar valores
    title = request.form.get('title', '').strip()
    target_value = request.form.get('target_value', '').strip()
    current_value = request.form.get('current_value', '').strip()
    unit = request.form.get('unit', '').strip()
    
    try:
        if title:
            goal.title = title
        if target_value:
            goal.target_value = float(target_value)
        if current_value:
            goal.current_value = float(current_value)
        if unit:
            goal.unit = unit
        
        goal.update_progress()  # Recalcula porcentagem
        db.session.commit()
        flash('Meta atualizada com sucesso!', 'success')
    except ValueError:
        flash('Valores inválidos. Use apenas números.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar meta: {str(e)}', 'danger')
    
    return redirect(url_for('goals.index'))

@bp.route('/add-progress/<int:id>', methods=['POST'])
@login_required
def add_progress(id):
    """Adiciona incremento ao progresso (ex: +1 livro, +250ml)"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        increment = float(request.form.get('increment', 0))
        goal.current_value += increment
        
        # Não permitir valores negativos
        if goal.current_value < 0:
            goal.current_value = 0
        
        goal.update_progress()
        db.session.commit()
        
        flash(f'Progresso atualizado! +{increment} {goal.unit}', 'success')
    except ValueError:
        flash('Valor inválido.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro: {str(e)}', 'danger')
    
    return redirect(url_for('goals.index'))

@bp.route('/set-progress/<int:id>', methods=['POST'])
@login_required
def set_progress(id):
    """Define valor absoluto do progresso (ex: 3 livros de 12)"""
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    try:
        new_value = float(request.form.get('current_value', 0))
        
        if new_value < 0:
            new_value = 0
        
        goal.current_value = new_value
        goal.update_progress()
        db.session.commit()
        
        flash('Progresso atualizado com sucesso!', 'success')
    except ValueError:
        flash('Valor inválido.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro: {str(e)}', 'danger')
    
    return redirect(url_for('goals.index'))

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    goal = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(goal)
    db.session.commit()
    flash('Meta excluída com sucesso.', 'success')
    return redirect(url_for('goals.index'))