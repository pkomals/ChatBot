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
            'Order Remove': remove_from_order,
            'track.order - context: ongoing-tracking': track_order
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

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
        })
    
    food_items = parameters["fooditems"]
    current_order = inprogress_orders[session_id]

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'

    if len(no_such_items) > 0:
        fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = utils.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what is left in your order: {order_str}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

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

def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
