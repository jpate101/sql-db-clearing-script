# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:52:44 2024

@author: JoshuaPaterson
"""

import mysql.connector
import time

# MySQL server connection configuration
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'testing',
    'raise_on_warnings': True,
    'connection_timeout': 10
}

# Define the queries to be executed
query = "SELECT * FROM test_table LIMIT 1"
query2 = "DELETE FROM test_table LIMIT 1"
query3 = "INSERT INTO test_table (message) VALUES ('Message #')"

def execute_query(connection, cursor, query):
    try:
        cursor.execute(query3)
        
        if query.startswith("SELECT"):
            rows = cursor.fetchall()
            if rows:
                print("Query executed successfully. Result:")
                for row in rows:
                    print(row)
            else:
                print("No data found for SELECT query.")
        
        elif query.startswith("DELETE") or query.startswith("INSERT"):
            # Get the number of affected rows
            affected_rows = cursor.rowcount
            
            if affected_rows > 0:
                connection.commit()
                print(f"Query executed successfully. {affected_rows} row(s) affected.")
            else:
                print("No rows were affected by the query.")
    
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        with open('error_log.txt', 'a') as f:
            f.write(f"Error executing query: {err}\n")

def main():
    while True:
        try:
            # Connect to MySQL server
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            # Execute the queries
            execute_query(connection, cursor, query2)
            print("-----  ")

            # Close cursor and connection
            cursor.close()
            connection.close()
        
        except mysql.connector.Error as err:
            print(f"MySQL connection error: {err}")
            time.sleep(5)  # Wait for 5 seconds before retrying
        
        time.sleep(1)  # Wait for 5 seconds before retrying

if __name__ == "__main__":
    main()