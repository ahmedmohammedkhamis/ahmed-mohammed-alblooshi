
from fastapi import FastAPI, Body
from datetime import datetime

app = FastAPI()

@app.post("/echo")
def echo(message: str = Body(embed=True)):
    return {
        "message": message,
        "timestamp": datetime.now().astimezone().isoformat()
    }
