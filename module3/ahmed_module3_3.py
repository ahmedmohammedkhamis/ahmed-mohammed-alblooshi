
from fastapi import FastAPI, Body

app = FastAPI()

@app.post("/check")
def check(Text: str = Body(embed=True)):
    return {"message": "Success", "Text": Text}
