import sqlite3
import functools

# Simple logger using print (or use logging module)
def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"Executing SQL query: {query}")
        return func(query, *args, **kwargs)  # pass arguments and return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Test it
users = fetch_all_users(query="SELECT * FROM users")
print(users)