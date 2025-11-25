def stream_user_ages():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    query = "SELECT age FROM user_data;"
    cursor.execute(query)

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()

def average_age():
    total=0
    count=0
    for age in stream_user_ages():
        count+=1
        total += age

    try:
        avg= total/count
        return avg
    except ZeroDivisionError as e:
        print(e)

if __name__ == "__main__":
    average_age = average_age()
    print(f"Average age of users: {average_age:.2f}")
