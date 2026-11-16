
from fastapi import FastAPI, Request
import logging

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("my_file.log"),
        logging.StreamHandler()
    ]
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception:
        status = 500
        logging.info(f"{request.method} {request.url.path} {status}")
        raise

    logging.info(f"{request.method} {request.url.path} {status}")
    return response

@app.get("/hello")
def hello():
    return {"message": "Hello Ahmed"}
