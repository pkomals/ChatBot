# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db  # Import the db module we just updated
import utils


inprogress_orders = {}
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
        output_contexts = payload['queryResult']['outputContexts']
        session_id=utils.extract_session_id(output_contexts[0]['name'])

        intent_handler_dict = {
        'Add Order': add_to_order,
        # 'order.remove - context: ongoing-order': remove_from_order,
        # 'order.complete - context: ongoing-order': complete_order,
        # 'track.order - context: ongoing-tracking': track_order
    }
        return intent_handler_dict[intent](parameters,session_id)
    

        # if intent == "track.order - context: ongoing-tracking":
        #     order_id = parameters["order_id"]
        #     status = db.get_order_status(order_id)
            
        #     if status:
        #         fulfillment_text = f"The status for order ID {order_id} is: {status}."
        #     else:
        #         fulfillment_text = f"No order found with ID {order_id}."

        #     return JSONResponse(content={"fulfillmentText": fulfillment_text})
        
        # return JSONResponse(content={"fulfillmentText": "Intent not recognized."})

    except Exception as e:
        print(f"Error in handling request: {e}")
        return JSONResponse(content={"fulfillmentText": "An error occurred while processing your request."}, status_code=500)

def add_to_order(parameters:dict, session_id:str):
    food_items=parameters["FoodItems"]
    quantities= parameters["number1"]
        
    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_dict = dict(zip(food_items, quantities))
        if session_id in inprogress_orders:
            current_food_dict= inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
        else:
            inprogress_orders[session_id]=new_food_dict

        order_str=utils.get_str_from_food_dict(inprogress_orders[session_id])

        fulfillment_text=f"so far you have {order_str} in your cart do you need anythin else?"
    return JSONResponse(content={"fulfillmentText": fulfillment_text})

# def save_to_order():

#     return



# def complete_order(parameters: dict, session_id: str):
#     if session_id not in inprogress_orders:
#         fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
#     else:
#         order = inprogress_orders[session_id]
#         # order_id = save_to_db(order) 