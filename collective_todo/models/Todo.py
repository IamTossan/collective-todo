from collective_todo import db

todoGroup = db.Table(
    'todoGroup',
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id'), primary_key=True),
    db.Column('todo_id', db.Integer, db.ForeignKey('todo.todo_id'), primary_key=True),
)

class Todo(db.Model):
    __tablename__ = 'todo'

    todo_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)

    groups = db.relationship(
        'Group',
        secondary=todoGroup,
        lazy='subquery',
        backref=db.backref('groups', lazy=True),
        cascade='delete',
    )

    def __repr__(self):
        return '<Todo %r>' % self.text
