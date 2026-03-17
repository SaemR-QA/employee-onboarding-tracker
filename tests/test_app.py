import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from models import db, User, Employee


from models import db, User, Employee   # ← add Employee here


@pytest.fixture
def client():
    test_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_app.db"))

    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{test_db_path}"

    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

        admin = User(email="admin@test.com", role="admin")
        admin.set_password("Admin123!")

        user = User(email="user@test.com", role="user")
        user.set_password("User123!")

        employee = Employee(
            full_name="Test Employee",
            email="test@example.com",
            department="IT",
            start_date="2026-01-01",
            status="Active",
        )

        db.session.add(admin)
        db.session.add(user)
        db.session.add(employee)   # ← add it here
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()

    if os.path.exists(test_db_path):
        os.remove(test_db_path)


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_invalid_login(client):
    response = client.post(
        "/login",
        data={"email": "wrong@test.com", "password": "wrongpass"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_admin_login_success(client):
    response = client.post(
        "/login",
        data={"email": "admin@test.com", "password": "Admin123!"},
        follow_redirects=True,
    )
    assert response.status_code == 200


def test_user_cannot_delete_employee(client):
    # login as normal user
    client.post(
        "/login",
        data={"email": "user@test.com", "password": "User123!"},
        follow_redirects=True,
    )

    # attempt to delete employee with ID 1
    response = client.post("/employees/1/delete")

    assert response.status_code == 403