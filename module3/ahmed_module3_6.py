
from fastapi import FastAPI, Query

app = FastAPI()

items = list(range(1, 21))

@app.get("/items")
def get_items(
    page: int = Query(1, ge=1),
    size: int = Query(5, ge=1)
):
    total = len(items)
    start = (page - 1) * size
    end = start + size

    return {
        "page": page,
        "size": size,
        "total_items": total,
        "total_pages": (total + size - 1) // size,
        "items": items[start:end]
    }
