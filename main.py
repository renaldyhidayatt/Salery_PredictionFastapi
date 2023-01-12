import uvicorn
import numpy as np
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pickle

app = FastAPI()
model = pickle.load(open("model.pkl", "rb"))

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request):
    data = await request.json()
    int_features = [int(x) for x in data.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)
    return templates.TemplateResponse(
        "index", {"request": request, "prediction_text": "Salary is {}".format(output)}
    )


@app.post("/predict_api")
async def predict_api(request: Request):
    data = await request.json()
    prediction = model.predict([np.array(list(data.values()))])
    output = prediction[0]
    return {"output": output}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
