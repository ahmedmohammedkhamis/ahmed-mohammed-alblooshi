
from fastapi import FastAPI, Body, HTTPException
import random

app = FastAPI()

person = {}

@app.post("/person")
def save_person(name: str = Body(...), phone_number: str = Body(...)):
    person["name"] = name
    person["phone_number"] = phone_number
    return {"message": "Person saved", "person": person}

@app.get("/person")
def get_person():
    if not person:
        raise HTTPException(status_code=404, detail="No person saved")

    return {
        "name": person["name"],
        "phone_number": person["phone_number"],
        "random_number": random.randint(1, 100)
    }
