import sys
from pathlib import Path

from fastapi import FastAPI

from app.api.routes import users, text, image
from app.database import engine, Base


#creates the tables in the DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/api/users", tags=["User Management"])
app.include_router(text.router, prefix="/api/text", tags=["Text Moderation"])
app.include_router(image.router, prefix="/api/image", tags=["Image Moderation"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AIPCMS API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)