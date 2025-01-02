from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from sqlmodel import SQLModel, Session, create_engine, select
from sqlalchemy.orm import selectinload

from schemas import Car, CarOutput, Trip

engine = create_engine("sqlite:///carsharing.db", connect_args={"check_same_thread": False}, echo=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # app starting
    SQLModel.metadata.create_all(engine)
    yield
    # app shutting down

app = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def welcome(name):
    return {'message': f'Welcome {name} to car sharing service!'}

@app.get("/cars")
def get_cars(size: str = None, doors: int = None, session: Session = Depends(get_session)) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)
    return session.exec(query).all()


@app.get('/cars/{id}', response_model=CarOutput)
def get_car_by_id(id: int, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No cars with id {id}")


@app.post('/cars', response_model=Car)
def add_car(car: Car, session: Session = Depends(get_session)) -> Car:
    new_car = Car.model_validate(car)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car

@app.delete('/cars', response_model=Car)
def delete_car(id: int, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No cars with id {id}")

@app.put('/cars', response_model=Car)
def edit_car(id: int, new_data: Car, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        session.commit()
        session.refresh(car)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id={id}")

@app.post('/cars/{car_id}/trips', response_model=Trip)
def add_trip(car_id: int, trip_input: Trip, session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.model_validate(trip_input, update={'car_id': car_id})
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={car_id}.")


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)