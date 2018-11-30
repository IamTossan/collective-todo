from collective_todo import db
from wtforms import Form, validators, StringField, PasswordField

userNameMaxLength = 50

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(userNameMaxLength))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    group = db.relationship('Group', backref='owner', lazy=True, cascade='delete')

    def __repr__(self):
        return '<User %r>' % self.name

class CreateUserForm(Form):
    name = StringField('name', [validators.InputRequired(), validators.Length(min=4, max=userNameMaxLength)])
    password = PasswordField('password', [validators.InputRequired()])