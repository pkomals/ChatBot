# 


# import mysql.connector

# try:
#     # Attempt to connect to the database
#     cnx = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="admin",
#         database="pandeyji_eatery",
#         port=3306  # Ensure the port is explicitly specified
#     )
#     print("Connected to the database successfully!")
    
#     # Fetch data from a table for testing
#     cursor = cnx.cursor()
#     cursor.execute("SELECT * FROM order_tracking LIMIT 1;")
#     result = cursor.fetchall()
    
#     if result:
#         print("Data retrieved:", result)
#     else:
#         print("Table is empty or query returned no results.")

#     # Close connection
#     cursor.close()
#     cnx.close()

# except mysql.connector.Error as err:
#     print(f"Error: {err}")


import mysql.connector
import os 
import sys
import pymysql
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("password")
db=os.getenv("db")

def get_db_connection():
    print("Connecting--> mysql")
    try:
        #print(f"Host: {host}, User: {user}, Password: {password}, DB: {db}")
        connection=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )
        # print("Connection established")
        # df=pd.read_sql_query("select * from order_tracking",mydb)
        # print(df.head())

        # return df #returning df to data ingestion(raw)

        if connection:
            print("Connection successful!")
        else:
            print("Connection unsuccessful.")
        return connection
       
    except Exception as e:
        raise Exception
    
if __name__ == "__main__":
    test_order_id = 41  # Replace with an actual order_id for testing
    print("Testing database connection and query execution:")
    status = get_db_connection()
    if status:
        print(f"Order ID {test_order_id} status: {status}")
    else:
        print(f"No order found with ID {test_order_id}")
