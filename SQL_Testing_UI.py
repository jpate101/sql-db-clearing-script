import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
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

# Initialize Tkinter
root = tk.Tk()
root.title("MySQL Query Executor")
root.geometry("800x600")

# Text entry for query
query_entry = tk.Entry(root, width=70)
query_entry.pack(pady=20)

# Label and Entry for delay between queries
delay_label = tk.Label(root, text="Delay (seconds):")
delay_label.pack()

delay_entry = tk.Entry(root, width=10)
delay_entry.pack()

# Buttons for continuous execution
continuous_frame = tk.Frame(root)
continuous_frame.pack(pady=10)

def execute_single_query():
    global query_counter
    query = query_entry.get().strip()
    if query:
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            cursor.execute(query)

            if query.upper().startswith("SELECT"):
                rows = cursor.fetchall()
                if rows:
                    message = "Query executed successfully. Result:"
                    print(message)
                    message_label.config(text=message)
                    result_text.delete(1.0, tk.END)  # Clear previous results
                    for row in rows:
                        result_text.insert(tk.END, f"{row}\n")
                else:
                    message = "Query executed successfully. No results."
                    print(message)
                    message_label.config(text=message)
                    result_text.delete(1.0, tk.END)  # Clear previous results
            elif query.upper().startswith("DELETE") or query.upper().startswith("INSERT"):
                affected_rows = cursor.rowcount
                connection.commit()
                message = f"Query executed successfully. {affected_rows} row(s) affected."
                print(message)
                message_label.config(text=message)
                update_query_counters(affected_rows)

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            message = f"Error executing query: {err}"
            print(message)
            message_label.config(text=message)
            with open('error_log.txt', 'a') as f:
                f.write(f"Error executing query: {err}\n")
            update_query_counters(-1)  # Update failed queries counter
    
    else:
        message = "Please enter a query."
        print(message)
        message_label.config(text=message)

# Function to update query counter label
def update_query_counters(affected_rows):
    global query_counter, failed_query_counter, zero_rows_counter
    query_counter += 1
    query_counter_label.config(text=f"Queries Executed: {query_counter}")
    
    if affected_rows == 0:
        zero_rows_counter += 1
        zero_rows_label.config(text=f"Queries Executed on 0 Rows: {zero_rows_counter}")
    elif affected_rows < 0:
        failed_query_counter += 1
        failed_query_label.config(text=f"Failed Queries: {failed_query_counter}")

# Function to execute queries continuously with delay
def execute_continuous():
    global continuous_execution
    delay = int(delay_entry.get()) if delay_entry.get().strip().isdigit() else 0  # Default delay of 1 second
    continuous_execution = True
    while continuous_execution:
        execute_single_query()
        time.sleep(delay)  # Adjust sleep time based on user input

# Function to stop continuous execution
def stop_continuous():
    global continuous_execution
    continuous_execution = False
    message = "Continuous execution stopped."
    print(message)
    message_label.config(text=message)

# Buttons for continuous execution
start_button = tk.Button(continuous_frame, text="Start Continuous Execution", command=lambda: threading.Thread(target=execute_continuous).start())
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(continuous_frame, text="Stop Continuous Execution", command=stop_continuous)
stop_button.pack(side=tk.LEFT, padx=5)

# Button to execute query once
execute_once_button = tk.Button(root, text="Execute Once", command=execute_single_query)
execute_once_button.pack(pady=10)

# Label to display error or success messages
message_label = tk.Label(root, text="", fg="black")
message_label.pack()

# Counter for executed queries
query_counter = 0
query_counter_label = tk.Label(root, text=f"Queries Executed: {query_counter}")
query_counter_label.pack()

# Counter for failed queries
failed_query_counter = 0
failed_query_label = tk.Label(root, text=f"Failed Queries: {failed_query_counter}")
failed_query_label.pack()

# Counter for queries executed on 0 rows
zero_rows_counter = 0
zero_rows_label = tk.Label(root, text=f"Queries Executed on 0 Rows: {zero_rows_counter}")
zero_rows_label.pack()

# Frame to display query results
result_frame = tk.Frame(root)
result_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Scrolled text area for displaying query results
result_text = tk.Text(result_frame, wrap=tk.WORD, height=20, width=100)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the result text area
result_scroll = tk.Scrollbar(result_frame, command=result_text.yview)
result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=result_scroll.set)

# Start Tkinter main loop
root.mainloop()