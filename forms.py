from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EmployeeForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    department = StringField("Department", validators=[DataRequired(), Length(min=2, max=100)])
    start_date = StringField("Start Date", validators=[DataRequired(), Length(min=2, max=20)])
    status = StringField("Status", validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField("Save")
