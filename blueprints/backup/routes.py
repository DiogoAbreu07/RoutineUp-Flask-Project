from . import backup_bp
import os, shutil
from datetime import datetime
from flask import current_app, send_file, request, redirect, url_for, abort
from flask_login import login_required
from extensions import db

@backup_bp.get("/backup")
@login_required
def backup():
    db_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]
    db_path = db_uri.removeprefix("sqlite:///")
    if not os.path.exists(db_path):
        with current_app.app_context(): db.create_all()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(db_path, as_attachment=True, download_name=f"routineup_backup_{ts}.db")

@backup_bp.post("/restore")
@login_required
def restore():
    db_uri = current_app.config["SQLALCHEMY_DATABASE_URI"]
    db_path = db_uri.removeprefix("sqlite:///")
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith((".db",".sqlite",".sqlite3")):
        abort(400, "Arquivo inválido")
    head = f.stream.read(16); f.stream.seek(0)
    if not head.startswith(b"SQLite format 3\x00"):
        abort(400, "Não é SQLite válido")
    tmp = db_path + ".uploadtmp"; f.save(tmp)
    db.session.remove(); db.engine.dispose()
    shutil.copyfile(tmp, db_path); os.remove(tmp)
    return redirect(url_for("tasks.index"))
