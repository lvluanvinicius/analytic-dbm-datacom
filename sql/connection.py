import mysql.connector

class MysqlConnection(object):
    
    def __init__(self, *args, **kwargs):
        self.HOST = "0.0.0.0" 
        self.PORT = "33060" 
        self.USERNAME = "root" 
        self.PASSWORD = ""
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

    