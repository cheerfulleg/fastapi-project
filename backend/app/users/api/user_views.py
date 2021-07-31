from fastapi import APIRouter, BackgroundTasks
from fastapi_mail import MessageSchema
from starlette.responses import JSONResponse

from backend.app.auth.jwt import auth_jwt
from backend.app.users.schemas import User_Pydantic, User, UserDefaultIn_Pydantic, ResetPassword
from backend.app.users.utils import create_password_hash
from backend.config.settings import fm

user_router = APIRouter()


@user_router.post('', response_model=User_Pydantic, status_code=201)
async def create_user(new_user: UserDefaultIn_Pydantic):
    """
    Register new user
    - **username**: string 50 characters (no validation)
    - **email**: string 120 characters (validating)
    - **password_hash**: any password that will be hashed
    """
    password_hash = await create_password_hash(new_user.password_hash)
    user_obj = await User.create(username=new_user.username, email=new_user.email, password_hash=password_hash)
    return await User_Pydantic.from_tortoise_orm(user_obj)


@user_router.post("/reset-password")
async def reset_password(email: str, background_tasks: BackgroundTasks):
    user = await User.get(email=email)
    payload = {'id': user.id}
    reset_token = auth_jwt.create_access_token(payload)

    html = ('\n'
            '    Hi, you requested to reset your account password\n'
            '    Please, click the link to change your password\n'
            '    http://127.0.0.1:8000/users/reset-password/{}        \n'
            '    ').format(reset_token)

    message = MessageSchema(
        subject="Reset your password",
        recipients=[email],
        body=html,
        subtype="html"
    )

    background_tasks.add_task(fm.send_message, message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@user_router.post("/reset-password/{token}")
async def reset_password(token: str, data: ResetPassword):
    payload = auth_jwt.decode_token(token)
    password_hash = await create_password_hash(data.password)
    await User.filter(id=payload.get('id')).update(password_hash=password_hash)
    return JSONResponse(status_code=200, content={'detail': 'password was changed'})
