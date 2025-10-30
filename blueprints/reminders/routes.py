from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Reminder
from . import reminders_bp

@reminders_bp.get("/")
@login_required
def index():
    items = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.remind_at.asc()).all()
    return render_template("reminders/index.html", items=items)

@reminders_bp.post("/create")
@login_required
def create():
    title = (request.form.get("title") or "").strip()
    when = request.form.get("remind_at") or ""
    try:
        remind_at = datetime.fromisoformat(when)
    except Exception:
        flash("Data/hora inválida.", "error"); return redirect(url_for("reminders.index"))
    r = Reminder(title=title, remind_at=remind_at, user_id=current_user.id)
    db.session.add(r); db.session.commit()
    return redirect(url_for("reminders.index"))

@reminders_bp.post("/toggle/<int:id>")
@login_required
def toggle(id):
    r = Reminder.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    r.done = not bool(r.done); db.session.commit()
    return redirect(url_for("reminders.index"))

@reminders_bp.post("/delete/<int:id>")
@login_required
def delete(id):
    r = Reminder.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(r); db.session.commit()
    return redirect(url_for("reminders.index"))
