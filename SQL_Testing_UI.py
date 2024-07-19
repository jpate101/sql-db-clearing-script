import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
from datetime import datetime

# Function to execute a single query
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
                    result_text.delete(1.0, tk.END)  # Clear previous results
                    for row in rows:
                        result_text.insert(tk.END, f"{row}\n")
                    
                    # Clear error display if results are shown
                    error_text.delete(1.0, tk.END)
                    
                else:
                    message = "Query executed successfully. No results."
                    print(message)
                    result_text.delete(1.0, tk.END)  # Clear previous results
                    error_text.delete(1.0, tk.END)   # Clear any previous errors
                
                # Update message label in UI
                message_label.config(text=message)
            
            elif query.upper().startswith("DELETE") or query.upper().startswith("INSERT"):
                affected_rows = cursor.rowcount
                connection.commit()
                message = f"Query executed successfully. {affected_rows} row(s) affected."
                print(message)
                message_label.config(text=message)
                update_query_counters(affected_rows)
                
                # Clear error display if no errors
                error_text.delete(1.0, tk.END)
            
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            message = f"Error executing query: {err}"
            print(message)
            message_label.config(text=message)
            
            # Clear result display on error
            result_text.delete(1.0, tk.END)
            
            # Display error in the error text area
            error_text.insert(tk.END, f"{message}\n")
            
            # Update message label in UI
            message_label.config(text=message)
            
            update_query_counters(-1)  # Update failed queries counter
            
            # Log error with timestamp to file
            log_error(message)

    else:
        message = "Please enter a query."
        print(message)
        message_label.config(text=message)

# Function to log errors with timestamps to a file
def log_error(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    with open('error_log.txt', 'a') as f:
        f.write(log_message)

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

# MySQL server connection configuration
config = {
    'user': 'root',
    'password': 'Jpate.101',
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

# Buttons for query execution
query_buttons_frame = tk.Frame(root)
query_buttons_frame.pack(pady=10)

# Button to execute query once
execute_once_button = tk.Button(query_buttons_frame, text="Execute Once", command=execute_single_query)
execute_once_button.pack(side=tk.LEFT, padx=5)

# Buttons for continuous execution
continuous_frame = tk.Frame(query_buttons_frame)
continuous_frame.pack(side=tk.LEFT, padx=5)

start_button = tk.Button(continuous_frame, text="Start Continuous Execution", command=lambda: threading.Thread(target=execute_continuous).start())
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(continuous_frame, text="Stop Continuous Execution", command=stop_continuous)
stop_button.pack(side=tk.LEFT, padx=5)

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

# Label to display error or success messages
message_label = tk.Label(root, text="", fg="black")
message_label.pack()


# Frame for results
result_frame = tk.Frame(root)
result_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Label for result section
result_label = tk.Label(result_frame, text="Query Result:")
result_label.pack()

# Scrolled text area for displaying query results
result_text = tk.Text(result_frame, wrap=tk.WORD, height=10, width=100)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the result text area
result_scroll = tk.Scrollbar(result_frame, command=result_text.yview)
result_scroll.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=result_scroll.set)

# Frame for error logs
error_frame = tk.Frame(root)
error_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Label for error section
error_label = tk.Label(error_frame, text="Errors:")
error_label.pack()

# Scrolled text area for displaying errors
error_text = tk.Text(error_frame, wrap=tk.WORD, height=10, width=100)
error_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the error text area
error_scroll = tk.Scrollbar(error_frame, command=error_text.yview)
error_scroll.pack(side=tk.RIGHT, fill=tk.Y)
error_text.config(yscrollcommand=error_scroll.set)



# Start Tkinter main loop
root.mainloop()