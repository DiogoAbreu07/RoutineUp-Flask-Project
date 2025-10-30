import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app
from sqlalchemy.engine import make_url
import sqlite3, os

app = create_app()
u = make_url(app.config["SQLALCHEMY_DATABASE_URI"])
assert u.get_backend_name() == "sqlite", f"Não é SQLite: {u}"
db_path = u.database
print("DB:", db_path)

os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
con = sqlite3.connect(db_path)
cur = con.cursor()

def table_cols(t: str):
    return [r[1] for r in cur.execute(f"PRAGMA table_info({t})")]

def has_table(t: str) -> bool:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (t,))
    return cur.fetchone() is not None

def drop_index(name: str):
    try:
        cur.execute(f"DROP INDEX IF EXISTS {name}")
    except Exception:
        pass

def col_exists(cols, name):
    return name in cols

cur.execute("PRAGMA foreign_keys=OFF;")

# === GOAL ===
if has_table("goal"):
    cols = table_cols("goal")
    # Vamos recriar sempre para garantir o schema final correto
    # Construímos um SELECT dinâmico com defaults onde a coluna não existir
    sel_id         = "id" if col_exists(cols,"id") else "NULL AS id"
    sel_title      = "COALESCE(title,'')" if col_exists(cols,"title") else "'' AS title"
    sel_progress   = "COALESCE(progress,0)" if col_exists(cols,"progress") else "0 AS progress"
    sel_created_at = "COALESCE(created_at,CURRENT_TIMESTAMP)" if col_exists(cols,"created_at") else "CURRENT_TIMESTAMP AS created_at"
    sel_due_date   = "due_date" if col_exists(cols,"due_date") else "NULL AS due_date"

    cur.executescript(f"""
CREATE TABLE IF NOT EXISTS goal_new (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL DEFAULT 1,
    title VARCHAR(255) NOT NULL,
    progress INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date DATE,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
INSERT INTO goal_new (id, user_id, title, progress, created_at, due_date)
SELECT {sel_id},
       1 AS user_id,
       {sel_title},
       {sel_progress},
       {sel_created_at},
       {sel_due_date}
FROM goal;
DROP TABLE goal;
ALTER TABLE goal_new RENAME TO goal;
""")
    drop_index("ix_goal_user_id")
    cur.execute("CREATE INDEX IF NOT EXISTS ix_goal_user_id ON goal(user_id)")

# === REMINDER ===
if has_table("reminder"):
    cols = table_cols("reminder")
    # SELECT dinâmico
    sel_id         = "id" if col_exists(cols,"id") else "NULL AS id"
    sel_title      = "COALESCE(title,'')" if col_exists(cols,"title") else "'' AS title"
    sel_remind_at  = "remind_at" if col_exists(cols,"remind_at") else "datetime('now') AS remind_at"
    sel_done       = "COALESCE(done,0)" if col_exists(cols,"done") else "0 AS done"
    sel_created_at = "COALESCE(created_at,CURRENT_TIMESTAMP)" if col_exists(cols,"created_at") else "CURRENT_TIMESTAMP AS created_at"

    cur.executescript(f"""
CREATE TABLE IF NOT EXISTS reminder_new (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL DEFAULT 1,
    title VARCHAR(255) NOT NULL,
    remind_at DATETIME NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
INSERT INTO reminder_new (id, user_id, title, remind_at, done, created_at)
SELECT {sel_id},
       1 AS user_id,
       {sel_title},
       {sel_remind_at},
       {sel_done},
       {sel_created_at}
FROM reminder;
DROP TABLE reminder;
ALTER TABLE reminder_new RENAME TO reminder;
""")
    drop_index("ix_reminder_user_id")
    cur.execute("CREATE INDEX IF NOT EXISTS ix_reminder_user_id ON reminder(user_id)")

cur.execute("PRAGMA foreign_keys=ON;")
con.commit()
con.close()
print("OK: goal/reminder ajustados")
