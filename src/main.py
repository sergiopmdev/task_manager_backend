from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from auth import auth_router

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")
