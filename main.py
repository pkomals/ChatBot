# main.py
# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# # import db
# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Food Tracking Bot!"}

# @app.post("/webhook")
# async def handle_request(request: Request):
#     try:
#         print("Webhook called!")
#         # Parse the JSON payload from the request
#         payload = await request.json()
#         print(f"Payload received: {payload}")
        
#         # Extracting intent and parameters
#         intent = payload['queryResult']['intent']['displayName']
#         parameters = payload['queryResult']['parameters']
        
#         # Handle the "track.order - context: ongoing-tracking" intent
#         if intent == "track.order - context: ongoing-tracking":
#             order_id = parameters['order_id']
#             status = db.get_order_status(order_id)
            
#             if status:
#                 fulfillment_text = f"The status for order ID {order_id} is: {status}."
#             else:
#                 fulfillment_text = f"No order found with ID {order_id}."
            
#             return JSONResponse(content={"fulfillmentText": fulfillment_text})
        
#         # Handle other intents if needed
#         return JSONResponse(content={"fulfillmentText": "Intent not recognized."})
    
#     except Exception as e:
#         print(f"Error in handling request: {e}")
#         return JSONResponse(content={"fulfillmentText": "An error occurred while processing your request."}, status_code=500)

# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import db

# app = FastAPI()

# @app.post("/")
# async def handle_request(request: Request):
#     payload = await request.json()

#     # Extract the necessary information from the payload
#     # based on the structure of the WebhookRequest from Dialogflow
#     intent = payload['queryResult']['intent']['displayName']
#     parameters = payload['queryResult']['parameters']
#     output_contexts = payload['queryResult']['outputContexts']
#     if intent=="track.order - context: ongoing-tracking":
#          response= track_order(parameters)
#          return response
  
    
# def track_order(parameters:dict):
#     order_id= parameters['order_id']

#     order_status= db.get_order_status(order_id)

#     if order_status:
#         fulfillment_text=f"The order status for order is {order_id}is :{order_status}"

#     else:
#         fulfillment_text=f"No order found with order id {order_id}"

#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text})

# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import db

# app = FastAPI()


# @app.post("/")
# async def handle_request(request: Request):
#     payload = await request.json()

#     # Extract the necessary information from the payload
#     # based on the structure of the WebhookRequest from Dialogflow
#     intent = payload["queryResult"]["intent"]["displayName"]
#     parameters = payload["queryResult"]["parameters"]
#     output_contexts = payload["queryResult"]["outputContexts"]

#     if intent == "track.order - context: ongoing-tracking":
#         response = await track_order(parameters)  # Use await for async function
#         return response

#     return JSONResponse(content={"message": "This intent is not supported yet."})  # Default response


# async def track_order(parameters: dict):
#     order_id = parameters["order_id"]

#     order_status = db.get_order_status(order_id)

#     if order_status:
#         fulfillment_text = f"The order status for order ID {order_id} is: {order_status}"
#     else:
#         fulfillment_text = f"No order found with order ID {order_id}"

#     return JSONResponse(content={"fulfillmentText": fulfillment_text})

# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db  # Import the db module we just updated

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Food Tracking Bot!"}

@app.post("/")
async def handle_request(request: Request):
    try:
        # Parse the JSON payload from the request
        payload = await request.json()
        intent = payload["queryResult"]["intent"]["displayName"]
        parameters = payload["queryResult"]["parameters"]

        if intent == "track.order - context: ongoing-tracking":
            order_id = parameters["order_id"]
            status = db.get_order_status(order_id)
            
            if status:
                fulfillment_text = f"The status for order ID {order_id} is: {status}."
            else:
                fulfillment_text = f"No order found with ID {order_id}."

            return JSONResponse(content={"fulfillmentText": fulfillment_text})
        
        return JSONResponse(content={"fulfillmentText": "Intent not recognized."})

    except Exception as e:
        print(f"Error in handling request: {e}")
        return JSONResponse(content={"fulfillmentText": "An error occurred while processing your request."}, status_code=500)
