from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import grader

app = FastAPI(title="Essay Grader API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grader.router)


@app.get("/health")
def health():
    return {"status": "ok"}