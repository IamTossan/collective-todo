import uuid
from werkzeug.security import generate_password_hash

from collective_todo import app, db
from collective_todo.models.User import User
from collective_todo.models.Group import Group

def create_superuser(name='root', password='root'):
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(
        public_id=str(uuid.uuid4()),
        name=name,
        password=hashed_password,
        admin=False,
    )

    db.session.add(new_user)
    db.session.flush()

    new_group = Group(
        name=name,
        owner=new_user,
    )

    new_group.users.append(new_user)
    db.session.add(new_group)
    db.session.commit()

    print('Superuser created!')
