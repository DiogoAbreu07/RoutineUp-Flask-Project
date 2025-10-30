import sys
import pathlib
from datetime import date, timedelta
from flask import render_template
from flask_mail import Message
from collections import defaultdict

# --- Configuração do Ambiente (similar ao fix_goal_reminder.py) ---
# Garante que a app pode ser importada
ROOT = pathlib.Path(__file__).resolve().parents[0]
sys.path.insert(0, str(ROOT))
# -----------------------------------------------------------------

from app import create_app
from extensions import db, mail
from models import User, Task

def find_upcoming_tasks():
    """
    Encontra todas as tarefas não concluídas que vencem hoje ou amanhã.
    """
    print("A procurar tarefas com prazo próximo...")
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Procura tarefas que não estão feitas (done=False) E
    # cujo prazo (due_date) é hoje OU amanhã.
    tasks = Task.query.filter(
        Task.done == False,
        Task.due_date.in_([today, tomorrow])
    ).all()
    
    print(f"Encontradas {len(tasks)} tarefas no total.")
    return tasks, today

def group_tasks_by_user(tasks):
    """
    Agrupa uma lista de tarefas por utilizador.
    """
    # Usamos defaultdict para criar automaticamente uma lista vazia 
    # para cada novo user_id
    tasks_by_user = defaultdict(list)
    for task in tasks:
        if task.user_id:
            tasks_by_user[task.user_id].append(task)
            
    print(f"Tarefas agrupadas por {len(tasks_by_user)} utilizadores.")
    return tasks_by_user

def send_email_alerts(tasks_by_user, today):
    """
    Envia um email de resumo para cada utilizador.
    """
    if not tasks_by_user:
        print("Nenhum utilizador para notificar.")
        return

    # Iteramos sobre cada ID de utilizador e a sua lista de tarefas
    for user_id, tasks in tasks_by_user.items():
        # Encontramos o objeto User para obter o email e o nome
        user = db.session.get(User, user_id)
        if not user or not user.email:
            print(f"Utilizador {user_id} não encontrado ou sem email. A saltar.")
            continue

        print(f"A preparar email para {user.email}...")

        try:
            # Renderiza o template HTML do email
            html_body = render_template(
                "email/due_date_alert.html",
                user=user,
                tasks=tasks,
                today=today,
                now=date.today() # Para o ano no rodapé
            )
            
            # Cria a mensagem de email
            msg = Message(
                subject="RoutineUp - Alerta de Prazos Próximos!",
                sender=mail.DEFAULT_SENDER,
                recipients=[user.email],
                html=html_body
            )
            
            # Envia o email
            mail.send(msg)
            print(f"Email enviado com sucesso para {user.email}.")

        except Exception as e:
            print(f"!!! ERRO ao enviar email para {user.email}: {e}")

def run_alerts():
    """
    Função principal para executar todo o processo.
    """
    print("--- A iniciar script de alertas de prazo [", date.today(), "] ---")
    
    # Precisamos do contexto da aplicação para aceder à base de dados
    # e às configurações de email.
    app = create_app()
    with app.app_context():
        tasks, today = find_upcoming_tasks()
        if not tasks:
            print("Nenhuma tarefa encontrada. A terminar.")
            return
            
        tasks_by_user = group_tasks_by_user(tasks)
        send_email_alerts(tasks_by_user, today)
        
    print("--- Script de alertas concluído ---")

# --- Bloco de Execução ---
if __name__ == "__main__":
    run_alerts()