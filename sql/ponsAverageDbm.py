import sys
sys.path.insert(0, "../")

from sql.connection import MysqlConnection

class PonsAverageDbm(object):
    def __init__(self):
        self.TABLE = "pons_average_dbm"
        
    def save(self, olt_name, pon, average):
        sqlclass = MysqlConnection()
        conn = sqlclass.connection()        
        if conn.is_connected():
            sql = f"""INSERT INTO pons_average_dbm (
                    OLT_NAME, PON, DBM_AVERAGE
                ) VALUES (
                %s, %s, %s
                )"""
            cursor = conn.cursor()
            cursor.execute(sql, (olt_name, pon, average))
            conn.commit()
            cursor.close()
            
        else:
            print("Error: Banco de dados não conectado.")
            exit()
        