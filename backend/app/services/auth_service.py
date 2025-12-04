from ..models.user import User
from ..database import db

def register_user(username, password):
    if User.query.filter_by(username=username).first():
        raise ValueError("username_already_exists")
    
    user = User(username=username) # type: ignore
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    if not user.check_password(password):
        return None
    return user