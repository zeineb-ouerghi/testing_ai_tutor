from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, chat, modules

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Praxis AI Tutor")

origins = [
    "http://localhost:5173", # Vite default
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(modules.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Praxis API"}
