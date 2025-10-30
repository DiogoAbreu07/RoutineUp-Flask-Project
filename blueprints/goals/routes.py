from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Goal
from . import goals_bp

@goals_bp.get("/")
@login_required
def index():
    items = Goal.query.filter_by(user_id=current_user.id).order_by(Goal.created_at.desc()).all()
    return render_template("goals/index.html", items=items)

@goals_bp.post("/create")
@login_required
def create():
    title = (request.form.get("title") or "").strip()
    if not title:
        flash("Informe um título.", "error"); return redirect(url_for("goals.index"))
    g = Goal(title=title, user_id=current_user.id)
    db.session.add(g); db.session.commit()
    return redirect(url_for("goals.index"))

@goals_bp.post("/progress/<int:id>")
@login_required
def progress(id):
    g = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    try:
        g.progress = max(0, min(100, int(request.form.get("progress") or g.progress)))
    except Exception:
        pass
    db.session.commit()
    return redirect(url_for("goals.index"))

@goals_bp.post("/delete/<int:id>")
@login_required
def delete(id):
    g = Goal.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(g); db.session.commit()
    return redirect(url_for("goals.index"))
