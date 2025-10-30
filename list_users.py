from app import create_app
from extensions import db
from models import User
app = create_app()
with app.app_context():
    for u in User.query.order_by(User.id).all():
        print(f"id={u.id}  email={u.email}  name={u.name!r}")
