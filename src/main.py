from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.auth.router import auth_router
from src.tasks.router import tasks_router

app = FastAPI()

origins = ["http://localhost:3000", "https://task-manager-frontend-six.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")
