import mysql.connector


def stream_users():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
        )
        cursor = connection.cursor()
        cursor.execute("USE ALX_prodev;")
        cursor.execute("SELECT * from user_data")

        for row in cursor:
            yield row

        cursor.close()

    except mysql.connector.Error as e:
        print(f"Error during connection {e}")
        return None

    finally:
        if connection.is_connected():
            connection.close()


for user in stream_users():
    print(user)
