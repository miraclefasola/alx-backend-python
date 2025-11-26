import mysql.connector

class DatabaseConnection():
    def __init__(self, host, user, password,port,database):
        self.host= host
        self.user= user
        self.password= password
        self.port= port
        self.database=database

    def __enter__(self):
        try:
            self.conn= mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port= self.port,
                database=self.database,

            )
            self.cursor= self.conn.cursor()
            return self.cursor
        except mysql.connector.Error as e:
            print(f"Connection failed as a result of {e}")
           
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

with DatabaseConnection("localhost", "root", "password", "3306","alx_database") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)