from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.db_connection import db_connection
from app.routes import auth, chat, images
from app.config.firebase_config import initialize_firebase


async def lifespan(app:FastAPI):
    """Connect to MongoDB on startup and close on shutdown."""
    await db_connection.connect()
    initialize_firebase()
    yield
    await db_connection.close() 
app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from the API"}

app.include_router(auth.router)
app.include_router(images.router)
app.include_router(chat.router)