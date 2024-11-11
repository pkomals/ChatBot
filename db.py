# # import mysql.connector

# # def get_db_connection():
# #     """Create a new database connection."""
# #     print("Attempting to connect to the database...")
# #     return mysql.connector.connect(
# #         host="localhost",
# #         user="root",
# #         password="admin",
# #         database="pandeyji_eatery"
# #     )

# # def get_order_status(order_id):
# #     print("Connecting to database for order status...")
# #     cnx = get_db_connection()  # Create a new connection each time
# #     cursor = cnx.cursor()
    
# #     # Execute the SQL query to fetch the order status
# #     query = "SELECT status FROM order_tracking WHERE order_id = %s"
# #     print(f"Executing query: {query} with order_id: {order_id}")
# #     cursor.execute(query, (order_id,))
# #     result = cursor.fetchone()
    
# #     # Close the cursor and connection
# #     cursor.close()
# #     cnx.close()
    
# #     # Print result for debugging
# #     if result is not None:
# #         print(f"Order status found: {result[0]}")
# #         return result[0]
# #     else:
# #         print("No order found with the specified order_id.")
# #         return None

# # # Add this code for testing directly in the terminal
# # if __name__ == "__main__":
# #     test_order_id = 41  # Replace with an actual order_id for testing
# #     print("Testing database connection and query execution:")
# #     status = get_order_status(test_order_id)
# #     if status:
# #         print(f"Order ID {test_order_id} status: {status}")
# #     else:
# #         print(f"No order found with ID {test_order_id}")


# import mysql.connector
# from mysql.connector import Error

# def get_db_connection():
#     """Create a new database connection with detailed error messages."""
#     try:
#         print("Attempting to connect to the database...")
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="admin",
#             database="pandeyji_eatery"
#         )
#         if connection.is_connected():
#             print("Connection successful!")
#         else:
#             print("Connection unsuccessful.")
#         return connection
#     except Error as err:
#         print(f"Connection Error: {err}")
#         return None

# def get_order_status(order_id):
#     print("Connecting to database for order status...")
#     cnx = get_db_connection()
#     if cnx is None:
#         print("Failed to connect to the database.")
#         return None

#     try:
#         cursor = cnx.cursor()
        
#         # Execute the SQL query to fetch the order status
#         query = "SELECT status FROM order_tracking WHERE order_id = %s"
#         print(f"Executing query: {query} with order_id: {order_id}")
#         cursor.execute(query, (order_id,))
#         result = cursor.fetchone()
        
#         # Print result for debugging
#         if result is not None:
#             print(f"Order status found: {result[0]}")
#             return result[0]
#         else:
#             print("No order found with the specified order_id.")
#             return None
#     except Error as err:
#         print(f"Database query error: {err}")
#         return None
#     finally:
#         # Close the cursor and connection
#         cursor.close()
#         cnx.close()
#         print("Connection closed.")

# # Test database connection and query execution
# if __name__ == "__main__":
#     test_order_id = 41  # Replace with an actual order_id for testing
#     print("Testing database connection and query execution:")
#     status = get_order_status(test_order_id)
#     if status:
#         print(f"Order ID {test_order_id} status: {status}")
#     else:
#         print(f"No order found with ID {test_order_id}")


# db.py

import pymysql

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
        connection.close()

        # Return the order status if found
        if result:
            return result[0]
        else:
            return None

    except Exception as e:
        print(f"Database error: {e}")
        return None
