from collective_todo import db

userGroup = db.Table(
    'userGroup',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id'), primary_key=True),
)

class Group(db.Model):
    __tablename__ = 'group'

    group_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    users = db.relationship(
        'User',
        secondary=userGroup,
        lazy='subquery',
        backref=db.backref('users', lazy=True),
        cascade='delete',
    )

    def __repr__(self):
        return '<Group %r>' % self.name
