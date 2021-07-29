from passlib.handlers.bcrypt import bcrypt


async def create_password_hash(password):
    return bcrypt.hash(password)
