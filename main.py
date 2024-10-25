from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db
# import generic_helper

app= FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.post("/")
# async def handle_request(request: Request):
#     # Retrieve the JSON data from the request
#     payload = await request.json()

#     # Extract the necessary information from the payload
#     # based on the structure of the WebhookRequest from Dialogflow
#     intent = payload['queryResult']['intent']['displayName']
#     parameters = payload['queryResult']['parameters']
#     output_contexts = payload['queryResult']['outputContexts']
    
#     if intent=="track.order - context: ongoing-tracking":
#         trackorder(parameters)
#         #return JSONResponse(content={"fulfillmentText":f"received=={intent}==in backend"})
        

# def trackorder(parameters: dict):
#     order_id= parameters['order_id']
#     status= db.get_order_status(order_id)
#     if status:
#         fulfillmentText= f"The order Status for order_id:{order_id} is : {status}"
#     else:
#         fulfillmentText=f"No order found with order_id:{order_id}"
        
#     return JSONResponse(content={"fulfillmentText":fulfillmentText})
