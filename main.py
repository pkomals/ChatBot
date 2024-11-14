# # main.py

# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import db  # Import the db module we just updated
# import utils


# inprogress_orders = {}
# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Food Tracking Bot!"}

# @app.post("/")
# async def handle_request(request: Request):
#     try:
#         # Parse the JSON payload from the request
#         payload = await request.json()
#         intent = payload["queryResult"]["intent"]["displayName"]
#         parameters = payload["queryResult"]["parameters"]
#         output_contexts = payload['queryResult']['outputContexts']
#         session_id=utils.extract_session_id(output_contexts[0]['name'])

#         intent_handler_dict = {
#         'Add Order': add_to_order,
#         # 'order.remove - context: ongoing-order': remove_from_order,
#         # 'order.complete - context: ongoing-order': complete_order,
#         # 'track.order - context: ongoing-tracking': track_order
#     }
#         return intent_handler_dict[intent](parameters,session_id)
    

#         # if intent == "track.order - context: ongoing-tracking":
#         #     order_id = parameters["order_id"]
#         #     status = db.get_order_status(order_id)
            
#         #     if status:
#         #         fulfillment_text = f"The status for order ID {order_id} is: {status}."
#         #     else:
#         #         fulfillment_text = f"No order found with ID {order_id}."

#         #     return JSONResponse(content={"fulfillmentText": fulfillment_text})
        
#         # return JSONResponse(content={"fulfillmentText": "Intent not recognized."})

#     except Exception as e:
#         print(f"Error in handling request: {e}")
#         return JSONResponse(content={"fulfillmentText": "An error occurred while processing your request."}, status_code=500)

# def add_to_order(parameters:dict, session_id:str):
#     food_items=parameters["FoodItems"]
#     quantities= parameters["number1"]
        
#     if len(food_items) != len(quantities):
#         fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
#     else:
#         new_food_dict = dict(zip(food_items, quantities))
#         if session_id in inprogress_orders:
#             current_food_dict= inprogress_orders[session_id]
#             current_food_dict.update(new_food_dict)
#         else:
#             inprogress_orders[session_id]=new_food_dict

#         order_str=utils.get_str_from_food_dict(inprogress_orders[session_id])

#         fulfillment_text=f"so far you have {order_str} in your cart do you need anythin else?"
#     return JSONResponse(content={"fulfillmentText": fulfillment_text})

# def save_to_db(order: dict):
#     next_order_id = db.get_next_order_id()

#     # Insert individual items along with quantity in orders table
#     for food_item, quantity in order.items():
#         rcode = db.insert_order_item(
#             food_item,
#             quantity,
#             next_order_id
#         )

#         if rcode == -1:
#             return -1
        
#         # Now insert order tracking status
#     db.insert_order_tracking(next_order_id, "in progress")
#     # print(next_order_id)
    
#     return next_order_id


# def complete_order(parameters: dict, session_id: str):
#     if session_id not in inprogress_orders:
#         fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
#     else:
#         order = inprogress_orders[session_id]
#         order_id = save_to_db(order)
#         if order_id == -1:
#             fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
#                                "Please place a new order again"
#         else:
#             order_total = db.get_total_order_price(order_id)

#             fulfillment_text = f"Awesome. We have placed your order. " \
#                            f"Here is your order id # {order_id}. " \
#                            f"Your order total is {order_total} which you can pay at the time of delivery!"

#         del inprogress_orders[session_id]

#     return JSONResponse(content={
#         "fulfillmentText": fulfillment_text
#     })



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
        output_contexts = payload['queryResult'].get('outputContexts', [])
        
        # Ensure output_contexts is not empty before accessing
        if output_contexts:
            session_id = utils.extract_session_id(output_contexts[0]['name'])
        else:
            raise ValueError("Session ID not found in output contexts.")

        # Define intent handlers and ensure all intents are covered
        intent_handler_dict = {
            'Add Order': add_to_order,
            'Order Complete': complete_order,
            # Uncomment other intent handlers as implemented
            # 'order.remove - context: ongoing-order': remove_from_order,
            # 'track.order - context: ongoing-tracking': track_order
        }

        # Call the corresponding intent handler function
        if intent in intent_handler_dict:
            return intent_handler_dict[intent](parameters, session_id)
        else:
            # Return default response if intent is not found
            return JSONResponse(content={"fulfillmentText": "Intent not recognized."})

    except Exception as e:
        print(f"Error in handling request: {e}")
        return JSONResponse(content={"fulfillmentText": "An error occurred while processing your request."}, status_code=500)

# Function to handle 'Add Order' intent
def add_to_order(parameters: dict, session_id: str):
    try:
        food_items = parameters.get("FoodItems")
        quantities = parameters.get("number1")

        if len(food_items) != len(quantities):
            fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
        else:
            new_food_dict = dict(zip(food_items, quantities))
            if session_id in inprogress_orders:
                current_food_dict = inprogress_orders[session_id]
                current_food_dict.update(new_food_dict)
            else:
                inprogress_orders[session_id] = new_food_dict

            order_str = utils.get_str_from_food_dict(inprogress_orders[session_id])
            fulfillment_text = f"So far, you have {order_str} in your cart. Do you need anything else?"
        
        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    except Exception as e:
        print(f"Error in add_to_order: {e}")
        return JSONResponse(content={"fulfillmentText": "An error occurred while adding items to your order."})

# Function to save order to database
# def save_to_db(order: dict):
#     try:
#         next_order_id = db.get_next_order_id()

#         # Insert individual items in the orders table
#         for food_item, quantity in order.items():
#             rcode = db.insert_order_item(food_item, quantity, next_order_id)
#             if rcode == -1:
#                 raise Exception("Failed to insert order item.")
        
#         # Insert order tracking status
#         db.insert_order_tracking(next_order_id, "in progress")
        
#         return next_order_id

#     except Exception as e:
#         print(f"Error in save_to_db: {e}")
#         return -1

#running fine :1
# def save_to_db(order: dict):
#     try:
#         next_order_id = db.get_next_order_id()
#         if next_order_id is None:
#             raise Exception("Failed to retrieve next order ID from the database.")

#         # Log the order and order ID
#         print(f"Next Order ID: {next_order_id}")
#         print(f"Order to Save: {order}")

#         # Insert individual items along with quantity in the orders table
#         for food_item, quantity in order.items():
#             print(f"Inserting item: {food_item} with quantity: {quantity}")
#             rcode = db.insert_order_item(food_item, quantity, next_order_id)
#             if rcode == -1:
#                 raise Exception(f"Failed to insert order item: {food_item}")

#         # Now insert order tracking status
#         print(f"Inserting order tracking for Order ID: {next_order_id}")
#         db.insert_order_tracking(next_order_id, "in progress")
        
#         return next_order_id

#     except Exception as e:
#         print(f"Error in save_to_db: {e}")
#         return -1

def save_to_db(order: dict):
    try:
        connection = db.get_db_connection()
        cursor = connection.cursor()

        # Fetch next order ID
        next_order_id = db.get_next_order_id()
        print(f"Next Order ID: {next_order_id}")
        print(f"Order to Save: {order}")

        # Insert each item in the order
        for food_item, quantity in order.items():
            print(f"Inserting item: {food_item} with quantity: {quantity}")

            # Call insert_order_item with connection and cursor
            rcode = db.insert_order_item(food_item, quantity, next_order_id, connection, cursor)

            # If insertion fails, handle rollback and exit
            if rcode == -1:
                raise Exception(f"Failed to insert order item: {food_item}")

        # Insert tracking information only if all items were added successfully
        db.insert_order_tracking(next_order_id, "in progress")

        # Commit the transaction after all inserts succeed
        connection.commit()
        print(f"Order {next_order_id} saved successfully!")

        return next_order_id

    except Exception as e:
        print(f"Error in save_to_db: {e}")
        try:
            # Rollback if any error occurs
            connection.rollback()
            print("Transaction rolled back due to an error.")
        except Exception as rollback_err:
            print(f"Error during rollback: {rollback_err}")
        return -1

    finally:
        cursor.close()
        connection.close()


# Function to handle 'Complete Order' intent
def complete_order(parameters: dict, session_id: str):
    try:
        if session_id not in inprogress_orders:
            fulfillment_text = "I'm having trouble finding your order. Please place a new order."
        else:
            order = inprogress_orders[session_id]
            order_id = save_to_db(order)
            if order_id == -1:
                fulfillment_text = "Sorry, I couldn't process your order due to a backend error. Please place a new order."
            else:
                order_total = db.get_total_order_price(order_id)
                fulfillment_text = (f"Your order has been placed! Your order ID is #{order_id}. "
                                    f"The total is {order_total}, payable at delivery.")
            del inprogress_orders[session_id]

        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    except Exception as e:
        print(f"Error in complete_order: {e}")
        return JSONResponse(content={"fulfillmentText": "An error occurred while completing your order."})

