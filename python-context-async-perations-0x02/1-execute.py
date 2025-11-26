import mysql.connector

class ExecuteQuery():
    def __init__(self, host, user, password,port,database, query, params):
        self.host= host
        self.user= user
        self.password= password
        self.port= port
        self.database=database
        self.query=query
        self.params = params

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
            self.cursor.execute(self.query, self.params)
            result= self.cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print(f"Connection failed as a result of {e}")
           
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

query = "SELECT * FROM users WHERE age > %s"
params = (25,)

with ExecuteQuery("localhost", "root", "password", "3306","alx_database", query) as results:

    print(results)

