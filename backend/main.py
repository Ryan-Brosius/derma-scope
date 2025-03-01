from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static frontend files
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/api/hello")
async def read_root():
    return {"message": "Hello from FastAPI!"}
