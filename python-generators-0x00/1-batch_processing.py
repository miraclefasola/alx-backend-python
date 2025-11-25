import mysql.connector

def stream_users_in_batches(batch_size):
    try:
        connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
        )
        cursor=connection.cursor()
        offset=0
        while True:
            cursor.execute("USE ALX_prodev;")
            query= f"SELECT * from user_data ORDER BY user_id LIMIT {batch_size} offset {offset};"
            cursor.execute(query)
            rows= cursor.fetchall()
            if not rows:
                break
            for row in rows:
                yield row
            offset+=batch_size

            cursor.close()


    except mysql.connector.Error as e:
        print(F"Error during connection {e}")
        return None

        
    finally:
            if connection.is_connected():
                connection.close()


def batch_processing(batch_size):
    for row in stream_users_in_batches(batch_size):
        if row[3]>25:
            yield row
   