from fastapi import FastAPI, Query, Path
from routers.aemet import router as aemetRouter

app = FastAPI()

@app.get("/")
def index():
    return {"mensaje":"Hello AEMET"}

app.include_router(aemetRouter)

#The required solution is hosted at /antartida (POST)
