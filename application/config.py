import os

from fastapi.templating import Jinja2Templates
from jinja2 import pass_context

# Constants
DB_URL = "sqlite://db.sqlite3"
DB_MODELS_DIR = "application/models"

JWT_SECRET_KEY = os.environ.get("JEWELLERY_HUB_JWT_KEY", "YOUR_JWT_KEY")
JWT_ALGORITHM = "HS256"

# Templates
templates = Jinja2Templates(directory="templates")

# Jinja2 url_for method fix for servers
# SERVER_NAME = os.uname()[1]

# default_url_for = templates.env.globals["url_for"]

# @pass_context
# def url_for(context: dict, name: str, **path_params) -> str:
#     path = default_url_for(context, name, **path_params).split("/")
#     return (
#         f"{path[0]}//{SERVER_NAME}/" +
#         "/".join(path[3:])
#     )

# templates.env.globals["url_for"] = url_for
