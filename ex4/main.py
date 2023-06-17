from uuid import UUID, uuid4
from datetime import datetime
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field


class BaseItem(BaseModel):
    id: UUID | None = Field(default_factory=uuid4)
    creation_date: datetime | None = Field(default_factory=datetime.now)


class ItemCreate(BaseItem):
    name: str
    description: str | None = None
    price: float
    tax: float | None = Field(default=None, description="Internal tax")


class ItemResponse(BaseItem):
    name: str
    description: str | None = None
    price: float


app = FastAPI()

items_database = {}


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    items_database[item.id] = item.dict(exclude={"id"})
    return item


@app.get("/items/", response_model=list[ItemResponse])
async def list_item():
    response = []
    for id, item in items_database.items():
        response.append(ItemResponse(id=id, **item))
    return response


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: UUID):
    if item_id in items_database:
        return items_database[item_id]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item com id={item_id} não encontrado!",
    )


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID):
    if item_id not in items_database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item com id={item_id} não encontrado!",
        )
    del items_database[item_id]
