import requests
import csv
import mysql.connector
import uuid


url = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20251125%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251125T130521Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=7d3dd2d5856790efd278519dd9c255d91400bf0279ebd7261178f3b41a7142f7"

response = requests.get(url)

with open("user_data.csv", "w", encoding="utf-8") as f:
    f.write(response.text)


def connectdb():
    try:
        connection = mysql.connector.connect(
            host="localhost", user="root", password="password"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"{e}")
        return None


def create_database(connection):

    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("ALX_prodev Database successfully created")
    except mysql.connector.Error as err:
        # Handle and report any database-specific error
        print(f"Error executing database command: {err}")
    finally:
        if cursor:
            cursor.close()


def create_table(connection):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("USE ALX_prodev;")
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                age INT UNSIGNED NOT NULL
            );
            """
            cursor.execute(create_table_sql)
            connection.commit()
            print("Table 'user_data' created successfully.")
        except mysql.connector.Error as e:
            print(f"Error in connectuion:{e}")
        finally:
            if cursor:
                cursor.close()


def insert_data(connection, csv_file):
    cursor = connection.cursor()

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            user_id = str(uuid.uuid4())

            query = """
            INSERT IGNORE INTO user_data(user_id, name, email, age)    
            VALUES(%s, %s, %s, %s)
            """
            cursor.execute("USE ALX_prodev;")
            cursor.execute(query, (user_id, row["name"], row["email"], row["age"]))

    connection.commit()
    cursor.close()


con = connectdb()
db = create_database(con)
table = create_table(con)
data_into = insert_data(con, "user_data.csv")
