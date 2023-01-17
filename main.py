from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import numpy as np
import pickle

app = FastAPI()
model = pickle.load(open("model.pkl", "rb"))


class Predict(BaseModel):
    year: float


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict_api")
async def predict_api(predict: Predict):
    prediction = model.predict(np.array([predict.year]).reshape(-1, 1))
    output = prediction[0]
    return {"output": output}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
