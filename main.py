from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import uvicorn
from sqlmodel import SQLModel, Session, create_engine

from schemas import Car, load_db, save_db

engine = create_engine("sqlite:///carsharing.db", connect_args={"check_same_thread": False}, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # app starting
    SQLModel.metadata.create_all(engine)
    yield
    # app shutting down

app = FastAPI(lifespan=lifespan)
db = load_db()



@app.get("/")
def welcome(name):
    return {'message': f'Welcome {name} to car sharing service!'}

@app.get("/cars")
def get_cars(size: str = None, doors: int = None) -> list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors: 
        result = [car for car in result if car.doors >= doors]
    return result


@app.get('/cars/{id}')
def get_car_by_id(id: int) -> Car:
    for car in db:
        if car.id == id:
            return car
    raise HTTPException(status_code=404, detail=f"No cars with id {id}")


@app.post('/cars', response_model=Car)
def add_car(car: Car) -> Car:
    with Session(engine) as session:
        new_car = Car.model_validate(car)
        session.add(new_car)
        session.commit()
        session.refresh()
        return new_car

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)