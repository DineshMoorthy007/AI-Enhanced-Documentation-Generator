from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="AI-Enhanced Documentation Generator")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}
