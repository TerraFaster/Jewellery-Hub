import time

from fastapi import APIRouter, Depends, Form, responses

from application.models import User


router = APIRouter(prefix="/api/v1/auth", tags=["api", "auth"])


class LoginForm:
    def __init__(
        self, 
        email: str = Form(), 
        password: str = Form()
    ):
        self.email = email.lower()
        self.password = password


class RegisterForm(LoginForm):
    def __init__(
        self, 
        username: str = Form(), 
        email: str = Form(), 
        password: str = Form()
    ):
        super().__init__(email, password)
        self.username = username


@router.post("/login")
async def login(
    user: User = Depends(User.dependency), 
    form_data: LoginForm = Depends()
):
    if user:
        return responses.JSONResponse({"error": "Already authorized"}, 400)

    user = await User.get_or_none(email=form_data.email)

    if user is None:
        return responses.JSONResponse({"error": "User not found"}, 404)

    if form_data.password != user.password:
        return responses.JSONResponse({"error": "Invalid password"}, 401)

    resp = responses.JSONResponse({"message": "Authorized"}, 200)
    resp.set_cookie(
        "Authorization", 
        user.generate_access_token(), 
    )

    return resp


@router.post("/register")
async def register(
    user: User = Depends(User.dependency), 
    form_data: RegisterForm = Depends()
):
    if user:
        return responses.JSONResponse({"error": "Already authorized"}, 400)

    if await User.exists(email=form_data.email):
        return responses.JSONResponse({"error": "User already exists"}, 400)

    user = await User.create(
        id=int(time.time() * 10**8), 
        username=form_data.username, 
        email=form_data.email, 
        password=form_data.password
    )

    resp = responses.JSONResponse({"message": "User created"}, 201)
    resp.set_cookie(
        "Authorization", 
        user.generate_access_token()
    )

    return resp
