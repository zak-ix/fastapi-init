from typing import Optional
from pydantic import BaseModel
import json
from sqlmodel import Field, SQLModel
from tomlkit import table

class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"


def load_db() -> list[Car]:
    with open("cars.json") as f:
        return [Car.model_validate(obj) for obj in json.load(f)]
    
def save_db(cars: list[Car]):
    with open("cars.json", "w") as f:
        json.dump([car.model_dump() for car in cars], f, indent=4)
