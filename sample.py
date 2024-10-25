from typing import Union

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

app1 = FastAPI()


@app1.get("/")
def read_root():
    return {"Hello": "World"}

@app1.post("/")
async def handle_request(request: Request):
    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    # based on the structure of the WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    
    if intent=="track.order - context: ongoing-tracking":
        # trackorder(parameters)
        return JSONResponse(content={"fulfillmentText":f"received=={intent}==in backend"})