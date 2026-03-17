from app import app
from models import db, User, Employee

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="admin@test.com").first():
        admin = User(email="admin@test.com", role="admin")
        admin.set_password("Admin123!")
        db.session.add(admin)

    if not User.query.filter_by(email="user@test.com").first():
        user = User(email="user@test.com", role="user")
        user.set_password("User123!")
        db.session.add(user)

    if Employee.query.count() == 0:
        employees = [
            Employee(full_name="Jane Doe", email="Jane@example.com", department="HR", start_date="2026-03-01", status="Active"),
            Employee(full_name="John Doe", email="John@example.com", department="IT", start_date="2026-03-05", status="Pending"),
        ]
        db.session.add_all(employees)

    db.session.commit()
    print("Database seeded successfully.")