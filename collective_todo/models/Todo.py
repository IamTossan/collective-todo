from collective_todo import db
from wtforms import Form, validators, StringField, FieldList

todoGroup = db.Table(
    'todoGroup',
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id'), primary_key=True),
    db.Column('todo_id', db.Integer, db.ForeignKey('todo.todo_id'), primary_key=True),
)

todoTextMaxLength = 50

class Todo(db.Model):
    __tablename__ = 'todo'

    todo_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(todoTextMaxLength))
    complete = db.Column(db.Boolean)

    groups = db.relationship(
        'Group',
        secondary=todoGroup,
        lazy='subquery',
        backref=db.backref('groups', lazy=True),
    )

    def __repr__(self):
        return '<Todo %r>' % self.text

class CreateTodoForm(Form):
    text = StringField('text', [validators.InputRequired(), validators.Length(min=3, max=todoTextMaxLength)])
    target = FieldList(StringField([validators.InputRequired()]), min_entries=1)