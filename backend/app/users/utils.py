from passlib.handlers.bcrypt import bcrypt


def create_password_hash(password):
    return bcrypt.hash(password)
