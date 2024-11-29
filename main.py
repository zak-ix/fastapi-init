from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

db = [{"id":1,"size":"L","fuel":"gasoline","doors":5,"transmission":"manual"},
{"id":2,"size":"M","fuel":"hybrid","doors":3,"transmission":"auto"},
{"id":3,"size":"M","fuel":"hybrid","doors":3,"transmission":"manual"},
{"id":4,"size":"XL","fuel":"electric","doors":5,"transmission":"manual"},
{"id":5,"size":"S","fuel":"gasoline","doors":3,"transmission":"auto"},
{"id":6,"size":"M","fuel":"gasoline","doors":3,"transmission":"auto"},
{"id":7,"size":"XS","fuel":"hybrid","doors":3,"transmission":"manual"},
{"id":8,"size":"XS","fuel":"hybrid","doors":5,"transmission":"auto"},
{"id":9,"size":"XL","fuel":"hybrid","doors":3,"transmission":"manual"},
{"id":10,"size":"XL","fuel":"electric","doors":5,"transmission":"manual"}]

@app.get("/")
def welcome(name):
    return {'message': f'Welcome {name} to car sharing service!'}

@app.get("/cars")
def get_cars(size: str = None, doors: int = None) -> list:
    result = db
    if size:
        result = [car for car in result if car['size'] == size]
    if doors: 
        result = [car for car in result if car['doors'] == doors]
    return result


@app.get('/cars/{id}')
def get_car_by_id(id: int) -> dict:
    for car in db:
        if car['id'] == id:
            return car
    raise HTTPException(status_code=404, detail=f"No cars with id {id}")

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)