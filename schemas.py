from typing import Optional
from sqlmodel import Field, Relationship, SQLModel



class Trip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start: int
    end: int
    description: str
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")

class Car(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"
    trips: list[Trip] = Relationship(back_populates="car")


class CarOutput(SQLModel):
    id: Optional[int]
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"
    trips: list[Trip]
