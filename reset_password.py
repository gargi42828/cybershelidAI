from backend.app.database.connection import SessionLocal
from backend.app.database.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

user = db.query(User).filter(User.username == "gargi1").first()

if user:
    new_password = "Gargi@12345"
    user.password = pwd_context.hash(new_password)
    db.commit()
    print("Password reset successfully!")
    print("Username: gargi")
    print("New password: Gargi@12345")
else:
    print("User 'gargi' not found.")

db.close()