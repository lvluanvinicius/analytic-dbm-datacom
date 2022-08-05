import mysql.connector

class MysqlConnection(object):
    
    def __init__(self, *args, **kwargs):
        self.HOST = "10.254.192.212" 
        self.PORT = "33061" 
        self.USERNAME = "root" 
        self.PASSWORD = "965700"
        self.DATABASE = "analytic_dbm"
    
    def __str__(self):
        return f"Config Mysql: [Host {self.host} and port {self.port}]"
    
    def connection(self):
        conn =  mysql.connector.connect(
            host=self.HOST,
            user=self.USERNAME,
            port=self.PORT,
            password=self.PASSWORD,
            database=self.DATABASE,
            auth_plugin='mysql_native_password'
        )    

        return conn

    



if __name__=="__main__":
    print("--------------------------")
    mysqlconn = MysqlConnection()
    conn = mysqlconn.connection()
    conn.get_server_info();
    if conn.is_connected():
        print("Banco de dados conectado")
        cursor = conn.cursor()
        cursor.execute("select * from onus")
        print(cursor.fetchall())