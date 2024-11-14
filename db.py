import pymysql

# global cnx

# Define a function to get the database connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="admin",
        db="pandeyji_eatery",
        port=3306  # Ensure to specify the port
    )

def get_order_status(order_id):
    try:
        # Connect to the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Execute the SQL query to fetch the order status
            query = "SELECT status FROM order_tracking WHERE order_id = %s"
            cursor.execute(query, (order_id,))
            result = cursor.fetchone()
        
        # Close the connection
        # connection.close()

        # Return the order status if found
        if result:
            return result[0]
        else:
            return None

    except Exception as e:
        print(f"Database error: {e}")
        return None
    
def get_next_order_id():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1

def insert_order_item(food_item, quantity, order_id, connection, cursor):
    try:
        # Call the stored procedure instead of running raw SQL
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))
        connection.commit()  # Commit the transaction

        print(f"Order item '{food_item}' inserted successfully with quantity {quantity} for order ID {order_id}!")
        return 1

    except pymysql.MySQLError as err:
        print(f"Error inserting order item '{food_item}': {err}")
        connection.rollback()  # Rollback in case of an error
        return -1
    
def get_total_order_price(order_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result = cursor.fetchone()[0]

    return result

def insert_order_tracking(order_id, status):
    connection = get_db_connection()
    cursor = connection.cursor()
    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    connection.commit()

    # Closing the cursor
    cursor.close()



if __name__ == "__main__":
    connection = get_db_connection()
    cursor = connection.cursor()

    print("Testing database functions...")
    order_id = get_next_order_id()
    print(f"Next order ID: {order_id}")

    status = get_order_status(order_id)
    print(f"Order status: {status}")

    result = insert_order_item("Pizza", 2, order_id,connection, cursor)
    print("Insert result:", "Success" if result == 1 else "Failure")

    total_price = get_total_order_price(order_id)
    print(f"Total order price for order {order_id}: {total_price}")
