﻿from . import users_bp
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
from extensions import db, login_manager   # <- inclui login_manager
from models import User

# -------- user loader exigido pelo Flask-Login --------
@login_manager.user_loader
def load_user(user_id: str):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None
# ------------------------------------------------------

def _sanitize_email(s: str) -> str:
    return (s or "").strip().lower()

@users_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("hub.index"))
    return render_template("users/login.html")

@users_bp.post("/login")
def login_post():
    email = _sanitize_email(request.form.get("email"))
    pw = request.form.get("password") or ""
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, pw):
        flash("Credenciais inválidas.", "error")
        return redirect(url_for("users.login"))
    remember = bool(request.form.get("remember"))
    login_user(user, remember=remember)
    return redirect(url_for("hub.index"))

@users_bp.get("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("hub.index"))
    return render_template("users/register.html")

@users_bp.post("/register")
def register_post():
    name  = (request.form.get("name") or "").strip()
    email = _sanitize_email(request.form.get("email"))
    pw    = request.form.get("password") or ""
    birth_raw = (request.form.get("birth_date") or "").strip()
    gender = (request.form.get("gender") or "").strip() or None

    if not name or len(name) < 2:
        flash("Informe um nome válido.", "error"); return redirect(url_for("users.register"))
    if not email or "@" not in email:
        flash("Informe um e-mail válido.", "error"); return redirect(url_for("users.register"))
    if len(pw) < 6:
        flash("A senha deve ter pelo menos 6 caracteres.", "error"); return redirect(url_for("users.register"))
    if User.query.filter_by(email=email).first():
        flash("Já existe um usuário com este e-mail.", "error"); return redirect(url_for("users.register"))

    birth_date = None
    if birth_raw:
        try:
            birth_date = datetime.strptime(birth_raw, "%Y-%m-%d").date()
        except ValueError:
            flash("Data de nascimento inválida.", "error"); return redirect(url_for("users.register"))

    User.create(email=email, password=pw, name=name, birth_date=birth_date, gender=gender)
    flash("Conta criada com sucesso. Você já pode entrar.", "info")
    return redirect(url_for("users.login"))

@users_bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))
