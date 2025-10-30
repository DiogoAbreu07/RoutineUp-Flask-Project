from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Task
from datetime import date, datetime
from sqlalchemy import case
from . import tasks_bp


@tasks_bp.get("/")
@login_required
def index():
    """Lista todas as tarefas do usuário com filtros e ordenação"""
    # Parâmetros de filtro e ordenação
    sort_param = request.args.get('sort', 'priority')
    filter_param = request.args.get('filter', 'pending')
    
    # Query base
    query = Task.query.filter_by(user_id=current_user.id)
    
    # Aplicar filtro
    if filter_param == 'pending':
        query = query.filter_by(done=False)
    elif filter_param == 'done':
        query = query.filter_by(done=True)
    # 'all' não precisa de filtro adicional
    
    # Aplicar ordenação
    if sort_param == 'priority':
        # Prioridade: Alta (2) -> Média (1) -> Baixa (0), depois por prazo
        query = query.order_by(
            Task.priority.desc(),
            case((Task.due_date.is_(None), 1), else_=0),
            Task.due_date.asc()
        )
    elif sort_param == 'due_date':
        # Prazo: Tarefas com prazo primeiro (do mais próximo ao mais distante), depois sem prazo
        query = query.order_by(
            case((Task.due_date.is_(None), 1), else_=0),
            Task.due_date.asc(),
            Task.priority.desc()
        )
    elif sort_param == 'created':
        # Criação: Mais recentes primeiro
        query = query.order_by(Task.created_at.desc())
    else:
        # Fallback para prioridade
        query = query.order_by(Task.priority.desc(), Task.created_at.desc())
    
    tasks = query.all()
    
    return render_template(
        "tasks/index.html",
        tasks=tasks,
        current_sort=sort_param,
        current_filter=filter_param
    )


@tasks_bp.post("/add")
@login_required
def add():
    """Adiciona uma nova tarefa"""
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date_str = request.form.get("due_date", "").strip()
    priority = request.form.get("priority", "1")
    done = request.form.get("done", "0")
    
    # Validação
    if not title:
        flash("O título da tarefa é obrigatório.", "error")
        return redirect(url_for("tasks.index"))
    
    # Converter prazo
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Data inválida.", "error")
            return redirect(url_for("tasks.index"))
    
    # Converter prioridade
    try:
        priority = int(priority)
        if priority not in [0, 1, 2]:
            priority = 1
    except ValueError:
        priority = 1
    
    # Converter status
    done = done == "1"
    
    # Criar tarefa
    task = Task(
        title=title,
        description=description if description else None,
        due_date=due_date,
        priority=priority,
        done=done,
        user_id=current_user.id,
        created_at=datetime.utcnow(),
        completed_at=datetime.utcnow() if done else None
    )
    
    db.session.add(task)
    db.session.commit()
    
    flash("Tarefa adicionada com sucesso!", "success")
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit(task_id):
    """Edita uma tarefa existente"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        flash("Tarefa não encontrada.", "error")
        return redirect(url_for("tasks.index"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date_str = request.form.get("due_date", "").strip()
        priority = request.form.get("priority", "1")
        done = request.form.get("done", "0")
        
        # Validação
        if not title:
            flash("O título da tarefa é obrigatório.", "error")
            return render_template("tasks/edit.html", task=task)
        
        # Atualizar título e descrição
        task.title = title
        task.description = description if description else None
        
        # Atualizar prazo
        if due_date_str:
            try:
                task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Data inválida.", "error")
                return render_template("tasks/edit.html", task=task)
        else:
            task.due_date = None
        
        # Atualizar prioridade
        try:
            priority = int(priority)
            if priority in [0, 1, 2]:
                task.priority = priority
        except ValueError:
            pass
        
        # Atualizar status
        new_done = done == "1"
        if new_done != task.done:
            task.done = new_done
            if new_done:
                task.completed_at = datetime.utcnow()
            else:
                task.completed_at = None
        
        db.session.commit()
        flash("Tarefa atualizada com sucesso!", "success")
        return redirect(url_for("tasks.index"))
    
    # GET: Renderiza o formulário de edição
    return render_template("tasks/edit.html", task=task)


@tasks_bp.post("/toggle/<int:task_id>")
@login_required
def toggle(task_id):
    """Marca/desmarca uma tarefa como concluída (form tradicional)"""
    sort_param = request.args.get('sort', 'priority')
    filter_param = request.args.get('filter', 'pending')
    redirect_url = url_for('tasks.index', sort=sort_param, filter=filter_param)
    
    t = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not t:
        flash("Tarefa não encontrada.", "error")
        return redirect(redirect_url)
    
    t.done = not t.done
    if t.done:
        t.completed_at = datetime.utcnow()
    else:
        t.completed_at = None
    
    db.session.commit()
    return redirect(redirect_url)


@tasks_bp.post("/delete/<int:task_id>")
@login_required
def delete(task_id):
    """Exclui uma tarefa"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    
    if not task:
        flash("Tarefa não encontrada.", "error")
        return redirect(url_for("tasks.index"))
    
    db.session.delete(task)
    db.session.commit()
    
    flash("Tarefa excluída com sucesso!", "success")
    return redirect(url_for("tasks.index"))


@tasks_bp.post("/api/toggle/<int:task_id>")
@login_required
def api_toggle(task_id):
    """API JSON para marcar/desmarcar tarefa (usado pelo JavaScript)"""
    t = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not t:
        return jsonify({"success": False, "error": "Tarefa não encontrada"}), 404
    
    try:
        t.done = not t.done
        new_state = t.done
        
        if t.done:
            t.completed_at = datetime.utcnow()
        else:
            t.completed_at = None
        
        db.session.commit()
        
        # Importar o helper format_due_date do app.py
        from app import format_due_date
        due_info = format_due_date(t.due_date, t.done, t.completed_at)
        
        return jsonify({
            "success": True,
            "new_state": new_state,
            "new_date_text": due_info.get('text', ''),
            "new_date_class": due_info.get('class', '')
        })
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao fazer toggle da tarefa {task_id}: {e}")
        return jsonify({"success": False, "error": "Erro ao atualizar a tarefa"}), 500