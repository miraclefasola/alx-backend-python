import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")  # open connection
        try:
            result = func(conn, *args, **kwargs)  # pass conn to the function
            return result
        finally:
            conn.close()  # close connection automatically
    return wrapper

def transactional(func):
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # run the DB operation
            conn.commit()  # commit changes if successful
            return result
        except Exception as e:
            conn.rollback()  # rollback if any error occurs
            print("Transaction rolled back due to:", e)
            raise  # re-raise the exception so caller knows
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')