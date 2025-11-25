import mysql.connector

def connectdb():
    try:
        connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
        )
        return connection
    except mysql.connector.Error as e:
        print(F"Error during connection {e}")
        return None

def stream_users(connection):
    cursor=connection.cursor()
    cursor.execute("USE ALX_prodev;")
    cursor.execute("SELECT * from user_data")

    for row in cursor:
        yield row


con = connectdb()

for user in stream_users(con):
    print(user)
