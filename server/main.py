from server.routes.chat_routes import router as chat_router
from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Agentic Chat API!"}


app.include_router(
    chat_router,
    prefix="/api",
    tags=["Chat"],
)
