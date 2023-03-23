from fastapi import APIRouter, Request, Depends, responses

from application.models import User
from application import config


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/logout")
async def logout(request: Request):
    response = responses.RedirectResponse(url=f"{router.prefix}/login", status_code=302)
    response.delete_cookie("Authorization")

    return response


@router.get("/{method}")
async def auth(request: Request, method: str, user: User = Depends(User.dependency)):
    if method not in ["login", "register"]:
        return responses.RedirectResponse(url=f"{router.prefix}/login", status_code=302)

    if user:
        return responses.RedirectResponse(url=request.url_for("index"), status_code=302)

    response = config.templates.TemplateResponse(
        "auth.html", 
        {"request": request, "method": method}
    )

    response.delete_cookie("Authorization")

    return response
