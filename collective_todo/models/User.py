from collective_todo import db

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    group = db.relationship('Group', backref='owner', lazy=True, cascade='delete')

    def __repr__(self):
        return '<User %r>' % self.name
