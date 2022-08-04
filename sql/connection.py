import mysql.connector

class Connection(object):
    
    def __init__(self, *args, **kwargs):
        self.host = "10.254.192.212" 
        self.port = "33061" 
        self.username = "root" 
        self.password = "965700"
        self.db = "analytic_dbm"
    
    def __str__(self):
        return f"Config Mysql: [Host {self.host} and port {self.port}]"
    
    def conn(self):
        return mysql.connector.connect(
            host=self.host, port=self.port, user=self.username, password=self.password,
            database=self.db, auth_plugin='mysql_native_password'
        )


if __name__=="__main__":
    connection = Connection()
    cursor = connection.conn().cursor()
    cursor.execute("SELECT * FROM onus")
    print(cursor)