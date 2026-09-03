from core.database import SessionLocal
from models.user import User
from models.category import Category

db = SessionLocal()

food = Category(name="Food", description="chicken with rice")
transport = Category(name="Transport", description="change the rings")

user = User(username="farbod", email="farbod@example.com")

db.add_all([food, transport, user])
db.commit()

print(f"User Created: ID = {user.id}")
print(f"Categories Created: ID 1 = {food.id}, ID 2 = {transport.id}")
db.close()
