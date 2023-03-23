import os
import uvicorn

from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise
from fastapi import FastAPI

from application import config, mixins
from application.util import import_module


app = FastAPI(openapi_url=None, docs_url=None, root_path="/")
app.mount("/static", StaticFiles(directory="static"), name="static")


def add_routers(app: FastAPI) -> None:
    for d in ["routers/frontend", "routers/api/v1"]:
        if not os.path.exists(d):
            continue
        
        for f in os.listdir(f"{d}"):
            if f.startswith("_") or not f.endswith(".py"):
                continue

            m = import_module(f"{d}/" + f)
            app.include_router(m.router)


async def connect_db() -> None:
    """
    Connect to the database.
    Load all models from the models folder and its subfolders.
    """
    await Tortoise.init(
        db_url=config.DB_URL,
        modules={
            "models": [
                f"{root}.{file[:-3]}".replace("\\", ".").replace("/", ".")
                for root, dirs, files in os.walk(config.DB_MODELS_DIR) 
                for file in files 
                if file.endswith(".py") and not file.startswith("_")
            ]
        }
    )
    await Tortoise.generate_schemas()


@app.on_event("startup")
async def startup() -> None:
    await connect_db()
    add_routers(app)


@app.on_event("shutdown")
async def shutdown() -> None:
    await Tortoise.close_connections()


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000)
