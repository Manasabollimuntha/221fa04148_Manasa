from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, ai_routes, reminder_routes

app = FastAPI(title="Agentic Financial Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(reminder_routes.router)
app.include_router(ai_routes.router)

@app.get("/")
def root():
    return {"message": "✅ Backend running successfully!"}
