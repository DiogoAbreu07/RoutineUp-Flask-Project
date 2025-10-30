from app import create_app
from extensions import db
from models import User, Task
app = create_app()
with app.app_context():
    print("Users:", db.session.query(User).count())
    print("Tasks:", db.session.query(Task).count())
