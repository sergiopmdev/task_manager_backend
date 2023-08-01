from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")
