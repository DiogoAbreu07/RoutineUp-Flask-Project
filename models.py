# ... (importações no topo) ...
from datetime import date, datetime
from flask_login import UserMixin
from sqlalchemy.sql import func
from extensions import db
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    # ... (código User inalterado) ...
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now) # Usando default python
    name = db.Column(db.String(120))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(20))
    avatar_filename = db.Column(db.String(80), nullable=True)

    tasks = db.relationship("Task", backref="owner", lazy="dynamic")
    goals = db.relationship("Goal", backref="owner", lazy="dynamic")
    reminders = db.relationship("Reminder", backref="owner", lazy="dynamic")

    @classmethod
    def create(cls, email: str, password: str, **extra):
        user = cls(email=(email or "").strip().lower(),
                   password_hash=generate_password_hash(password),
                   created_at=datetime.now(),
                   **extra)
        db.session.add(user); db.session.commit(); return user


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, nullable=False, server_default=db.text("0"))
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=True)
    priority = db.Column(db.Integer, nullable=False, server_default=db.text("1"))
    # --- NOVA COLUNA COMPLETED_AT ---
    completed_at = db.Column(db.DateTime, nullable=True) # Guarda quando foi concluída
    # --- FIM NOVA COLUNA ---

class Goal(db.Model): # Removido UserMixin desnecessário
    __tablename__ = "goal"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    progress = db.Column(db.Integer, nullable=False, server_default=db.text("0"))
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    due_date = db.Column(db.Date)

class Reminder(db.Model): # Removido UserMixin desnecessário
    __tablename__ = "reminder"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    remind_at = db.Column(db.DateTime, nullable=False)
    done = db.Column(db.Boolean, nullable=False, server_default=db.text("0"))
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())