from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from enum import Enum
from typing import Dict, Union, List, Optional


class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category


app = FastAPI()


items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0,
            category=Category.TOOLS),
    1: Item(name="Pliers", price=4.99, count=20, id=1,
            category=Category.TOOLS),
    2: Item(name="Nails", price=2.99, count=200, id=2,
            category=Category.CONSUMABLES)
}


SelectionType = Dict[str, Union[str, int, float, Category, None]]
"""
selection dictionary containing the user's query arguements.
The keys are of type str.
The values  can be of type str, int, float, Category or None
"""


@app.get("/")
def index() -> Dict[str, Dict[int, Item]]:
    return {"items": items}


@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail=f"Item with {item_id} does not exist"
        )
    return items[item_id]


@app.get("/items")
def query_item_by_parameters(name: Optional[str] = None,
                             price: Optional[float] = None,
                             count: Optional[int] = None,
                             category: Optional[Category] = None,
                             ) -> Dict[str, Union[SelectionType, List[Item]]]:
    def check_item(item: Item) -> bool:
        return all(
            (name is None or item.name == name,
             price is None or item.price == price,
             count is None or item.count == count,
             category is None or item.category is category,)
        )
    
    # Log the query parameters
    print(f"Query Parameters: name={name}, price={price}, count={count},\
          category={category}")
    selection = [item for item in items.values() if check_item(item)]
    print(f"selection: {selection}")
    print(type(selection))
    return {
        "query": {"name": name, "price": price, "count": count,
                  "category": category},

        "selection": selection,
    }


@app.post("/")
def add_item(item: Item) -> Dict[str, Item]:
    if item.id in items:
        raise HTTPException(
            status_code=400,
            detail=f"Item with {item.id=} already exists."
        )
    items[item.id] = item
    return {"added": item}


@app.put("/items/{item_id}")
def update(item_id: int,
           name: Optional[str] = None,
           price: Optional[float] = None,
           count: Optional[int] = None,
           ) -> Dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail=f"Item with {item_id=} does not exist."
        )
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code=400,
            detail="No parameters provided for update."
        )
    
    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"updated": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> Dict[str, Item]:
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail=f"Item with {item_id} does not exist."
        )
    item = items.pop(item_id)
    return {"deleted": item}