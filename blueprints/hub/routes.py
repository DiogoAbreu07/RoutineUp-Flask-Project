from datetime import date, datetime, time, timedelta
from flask import render_template, jsonify
from flask_login import login_required, current_user
from models import Task, Goal, Reminder
from sqlalchemy import func, and_, or_, case, extract
from extensions import db
from . import hub_bp

@hub_bp.get("/")
@login_required
def index():
    today = date.today()
    now = datetime.now()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)

    # Saudação
    greeting = "Olá"
    current_hour = now.hour
    if 5 <= current_hour < 12: 
        greeting = "Bom dia"
    elif 12 <= current_hour < 18: 
        greeting = "Boa tarde"
    else: 
        greeting = "Boa noite"
    
    today_formatted = today.strftime('%A, %d de %B')

    # Inicializa stats com TODOS os campos necessários
    stats = {
        'done_total': 0,
        'pending_total': 0,
        'active_goals': 0,
        'completion_rate': 0,
        'streak': 0,
        'tasks_this_week': 0,
        'tasks_completed_today': 0,
        'overdue_tasks': 0,
        'high_priority_pending': 0,
        'weekly_chart': [],
        'priority_distribution': {'low': 0, 'medium': 0, 'high': 0},
        'productivity_score': 0
    }

    # Calcula estatísticas com tratamento de erro
    try:
        # Total de tarefas concluídas
        stats['done_total'] = Task.query.filter_by(
            user_id=current_user.id, 
            done=True
        ).count()

        # Tarefas pendentes (hoje ou atrasadas)
        stats['pending_total'] = Task.query.filter(
            Task.user_id == current_user.id,
            Task.done == False,
            or_(Task.due_date == today, Task.due_date < today)
        ).count()

        # Metas ativas
        stats['active_goals'] = Goal.query.filter(
            Goal.user_id == current_user.id,
            Goal.progress < 100
        ).count()

        # Tarefas atrasadas
        stats['overdue_tasks'] = Task.query.filter(
            Task.user_id == current_user.id,
            Task.done == False,
            Task.due_date < today
        ).count()

        # Tarefas de alta prioridade pendentes
        stats['high_priority_pending'] = Task.query.filter(
            Task.user_id == current_user.id,
            Task.done == False,
            Task.priority == 2
        ).count()

        # Tarefas concluídas hoje
        stats['tasks_completed_today'] = Task.query.filter(
            Task.user_id == current_user.id,
            Task.done == True,
            func.date(Task.completed_at) == today
        ).count()

        # Taxa de conclusão
        total_tasks = Task.query.filter_by(user_id=current_user.id).count()
        if total_tasks > 0:
            stats['completion_rate'] = int((stats['done_total'] / total_tasks) * 100)

        # Distribuição por prioridade
        priority_query = db.session.query(
            Task.priority,
            func.count(Task.id)
        ).filter(
            Task.user_id == current_user.id,
            Task.done == False
        ).group_by(Task.priority).all()

        for priority, count in priority_query:
            if priority == 0:
                stats['priority_distribution']['low'] = count
            elif priority == 1:
                stats['priority_distribution']['medium'] = count
            elif priority == 2:
                stats['priority_distribution']['high'] = count

        # Tarefas esta semana
        week_start = today - timedelta(days=today.weekday())
        stats['tasks_this_week'] = Task.query.filter(
            Task.user_id == current_user.id,
            Task.done == True,
            func.date(Task.completed_at) >= week_start
        ).count()

        # Gráfico semanal (últimos 7 dias)
        weekly_data = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            
            completed = Task.query.filter(
                Task.user_id == current_user.id,
                Task.done == True,
                func.date(Task.completed_at) == day
            ).count()
            
            created = Task.query.filter(
                Task.user_id == current_user.id,
                func.date(Task.created_at) == day
            ).count()
            
            # Nomes dos dias em português
            dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
            dia_nome = dias_semana[day.weekday()]
            
            weekly_data.append({
                'day': dia_nome,
                'day_full': day.strftime('%d/%m'),
                'completed': completed,
                'created': created
            })
        
        stats['weekly_chart'] = weekly_data

        # Streak (dias consecutivos)
        streak = 0
        current_day = today
        while True:
            tasks_day = Task.query.filter(
                Task.user_id == current_user.id,
                Task.done == True,
                func.date(Task.completed_at) == current_day
            ).count()
            
            if tasks_day > 0:
                streak += 1
                current_day = current_day - timedelta(days=1)
            else:
                break
            
            if streak > 365:  # Limite de segurança
                break
        
        stats['streak'] = streak

        # Score de produtividade (0-100)
        score = 0
        
        # Taxa de conclusão (40 pontos)
        score += min(stats['completion_rate'] * 0.4, 40)
        
        # Tarefas hoje (20 pontos)
        if stats['tasks_completed_today'] > 0:
            score += min(stats['tasks_completed_today'] * 5, 20)
        
        # Streak (20 pontos)
        if stats['streak'] > 0:
            score += min(stats['streak'] * 2, 20)
        
        # Penalidade por atrasadas (até -20)
        score -= min(stats['overdue_tasks'] * 5, 20)
        
        # Bônus por alta prioridade (10 pontos)
        if stats['high_priority_pending'] == 0:
            score += 10
        
        stats['productivity_score'] = max(0, min(100, int(score)))

    except Exception as e:
        print(f"ERRO ao calcular estatísticas: {e}")
        import traceback
        traceback.print_exc()

    # Buscar itens para timeline
    day_tasks = []
    day_reminders = []
    atrasadas = []
    metas = []
    
    try:
        day_tasks = Task.query.filter(
            Task.user_id == current_user.id, 
            Task.done == False, 
            Task.due_date == today
        ).order_by(Task.priority.desc(), Task.created_at.asc()).all()
    except Exception as e: 
        print(f"Erro ao buscar tarefas do dia: {e}")

    try:
        day_reminders = Reminder.query.filter(
            Reminder.user_id == current_user.id, 
            Reminder.done == False,
            Reminder.remind_at >= now, 
            Reminder.remind_at <= end_of_day
        ).order_by(Reminder.remind_at.asc()).all()
    except Exception as e:
        print(f"Erro ao buscar lembretes: {e}")

    # Timeline
    timeline_items = []
    for task in day_tasks: 
        timeline_items.append({
            'type': 'task', 
            'time': datetime.combine(today, time(12, 0)), 
            'obj': task
        })
    for reminder in day_reminders: 
        timeline_items.append({
            'type': 'reminder', 
            'time': reminder.remind_at, 
            'obj': reminder
        })
    timeline_items.sort(key=lambda item: item['time'])

    try:
        atrasadas = Task.query.filter(
            Task.user_id == current_user.id, 
            Task.done == False,
            Task.due_date != None, 
            Task.due_date < today
        ).order_by(Task.priority.desc(), Task.due_date.asc()).all()
    except Exception as e: 
        print(f"Erro ao buscar atrasadas: {e}")

    try:
        metas = Goal.query.filter_by(user_id=current_user.id)\
                          .order_by(Goal.created_at.desc()).limit(3).all()
    except Exception as e:
        print(f"Erro ao buscar metas: {e}")

    return render_template("hub/index.html",
                           today=today,
                           today_formatted=today_formatted,
                           greeting=greeting,
                           stats=stats,
                           timeline_items=timeline_items,
                           atrasadas=atrasadas,
                           metas=metas)


@hub_bp.get("/api/stats")
@login_required
def api_stats():
    """API endpoint para retornar estatísticas em JSON"""
    today = date.today()
    # Aqui você pode chamar a mesma lógica de cálculo
    # Por enquanto retorna um dict vazio
    return jsonify({'message': 'API de estatísticas'})