from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Employee
from forms import LoginForm, EmployeeForm
from decorators import admin_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("employees"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("employees"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

@app.route("/employees")
@login_required
def employees():
    records = Employee.query.all()
    return render_template("employees.html", records=records)

@app.route("/employees/<int:employee_id>")
@login_required
def employee_detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template("employee_detail.html", employee=employee)

@app.route("/employees/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        existing = Employee.query.filter_by(email=form.email.data).first()
        if existing:
            flash("An employee with that email already exists.", "danger")
            return render_template("employee_form.html", form=form, title="Add Employee")

        employee = Employee(
            full_name=form.full_name.data,
            email=form.email.data,
            department=form.department.data,
            start_date=form.start_date.data,
            status=form.status.data
        )
        db.session.add(employee)
        db.session.commit()
        flash("Employee added successfully.", "success")
        return redirect(url_for("employees"))

    return render_template("employee_form.html", form=form, title="Add Employee")

@app.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        existing = Employee.query.filter(Employee.email == form.email.data, Employee.id != employee.id).first()
        if existing:
            flash("Another employee with that email already exists.", "danger")
            return render_template("employee_form.html", form=form, title="Edit Employee")

        employee.full_name = form.full_name.data
        employee.email = form.email.data
        employee.department = form.department.data
        employee.start_date = form.start_date.data
        employee.status = form.status.data

        db.session.commit()
        flash("Employee updated successfully.", "success")
        return redirect(url_for("employees"))

    return render_template("employee_form.html", form=form, title="Edit Employee")

@app.route("/employees/<int:employee_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee deleted successfully.", "success")
    return redirect(url_for("employees"))

@app.errorhandler(403)
def forbidden(error):
    return "<h1>403 Forbidden</h1><p>You do not have permission to access this page.</p>", 403

def seed_default_data():
    if not User.query.filter_by(email="admin@test.com").first():
        admin = User(email="admin@test.com", role="admin")
        admin.set_password("Admin123!")
        db.session.add(admin)

    if not User.query.filter_by(email="user@test.com").first():
        user = User(email="user@test.com", role="user")
        user.set_password("User123!")
        db.session.add(user)

    if Employee.query.count() == 0:
        employee1 = Employee(
            full_name="Jane Doe",
            email="jane@example.com",
            department="HR",
            start_date="2026-03-01",
            status="Active",
        )
        employee2 = Employee(
            full_name="John Doe",
            email="john@example.com",
            department="IT",
            start_date="2026-03-05",
            status="Pending",
        )
        db.session.add(employee1)
        db.session.add(employee2)

    db.session.commit()

with app.app_context():
    db.create_all()
    seed_default_data()

if __name__ == "__main__":
    app.run(debug=True)
