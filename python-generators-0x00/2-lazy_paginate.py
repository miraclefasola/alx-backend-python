import mysql.connector


def paginate_users(page_size, offset):
    """Fetch a single page of users from the database."""
    connection = mysql.connector.connect(
        host="localhost", user="root", password="password", database="ALX_prodev"
    )
    cursor = connection.cursor()
    query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """Generator that lazily fetches users page by page."""
    offset = 0

    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        for row in page:
            yield row
        offset += page_size
