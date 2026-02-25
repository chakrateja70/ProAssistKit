import uvicorn
from fastapi import FastAPI
from src.routes import router

app = FastAPI(
    title="Mail generator",
    description="A simple API to generate random email addresses.",
    version="1.0.0",
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)