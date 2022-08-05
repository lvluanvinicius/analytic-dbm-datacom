import sys
sys.path.insert(0, "../")

from sql.connection import MysqlConnection


class OnusModel(object):
    def __init__(self):
        self.TABLE = "onus_dbm"
        
    def save(self, data):
        sqlclass = MysqlConnection()
        conn = sqlclass.connection()        
        if conn.is_connected():
            sql = f"""INSERT INTO {self.TABLE} (
                    NAME, SERIAL, PON, DBM, ONUID
                ) VALUES (
                    %s, %s, %s, %s, %s
                )"""
            cursor = conn.cursor()
            cursor.execute(sql, (data["NAME"], data["SERIAL"], data["PON"], data["DBM"], data["ONUID"]))
            conn.commit()
            cursor.close()
            
        else:
            return "Error: Banco de dados não conectado."
        
