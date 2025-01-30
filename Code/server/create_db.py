from flask_app import app, db, bcrypt
from flask_app.models import User

app.app_context().push()

hashed_pw = bcrypt.generate_password_hash('password')
librarian_user = User(username='Librarian', email='admin@bookhub.com', password=hashed_pw, role='librarian')

db.create_all()
db.session.add(librarian_user)
db.session.commit()

print("Database created successfully!")
