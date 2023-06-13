import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from routers import llm

app = FastAPI()
app.include_router(llm.router)


""" @app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
 """

# CORS
# Needed for Javascript Browser
# TODO: add origins in the config file
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*.leximpact.dev",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
def root():
    return {"message": "please go to /docs"}


@app.get("/status", tags=["root"])
def status():
    return {"llm": 'true'}


def start_dev():
    """
    Launched with `XXXXX` at root level
    Only for DEV, don't use for production
    """
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
