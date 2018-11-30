from flask import jsonify , request
from collective_todo import app, db
from collective_todo.routes.auth import token_required
from collective_todo.models.User import User
from collective_todo.models.Todo import Todo, todoGroup, CreateTodoForm
from collective_todo.models.Group import Group

@app.route('/todo', methods=['GET'])
@token_required
def get_all_todos(current_user):
    todos = Todo.query.join(todoGroup).join(Group).join(User).filter(User.user_id==current_user.user_id).all()

    output = []

    for todo in todos:
        todo_data = {
            'id': todo.todo_id,
            'text': todo.text,
            'complete': todo.complete,
        }
        output.append(todo_data)

    return jsonify({'todos': output})

@app.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
    todo = Todo.query.join(todoGroup).join(Group).join(User).filter(User.user_id==current_user.user_id, Todo.todo_id==todo_id).first()


    if not todo:
        return jsonify({'message': 'Todo not found!'})

    todo_data = {
        'id': todo.todo_id,
        'text': todo.text,
        'complete': todo.complete,
    }

    return jsonify(todo_data)

@app.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user):
    data = request.get_json()

    form = CreateTodoForm(request.form)
    if not form.validate():
        return jsonify({'message': 'invalid payload'})

    target_groups = db.session.query(Group).filter(Group.group_id.in_(data['target'])).all()

    new_todo = Todo(text=data['text'], complete=False, groups=target_groups)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created!'})

@app.route('/todo/<todo_id>', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(todo_id=todo_id).first()

    if not todo:
        return jsonify({'message': 'Todo not found!'})

    todo.complete = True
    db.session.commit()
    return jsonify({'message': 'Todo has been completed!'})

@app.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    todo = Todo.query.filter_by(todo_id=todo_id).first()

    if not todo:
        return jsonify({'message': 'Todo not found!'})

    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted!'})
