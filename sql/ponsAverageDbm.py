import sys
sys.path.insert(0, "../")



class PonsAverageDbm(object):
    def __init__(self):
        self.TABLE = "pons_average_dbm"
        
    def save(self, data):
        sqlclass = MysqlConnection()
        conn = sqlclass.connection()        
        if conn.is_connected():
            sql = f"""INSERT INTO pons_average_dbm (
                    OLT_NAME, PON, DBM_AVERAGE
                ) VALUES (
                %s, %s, %s
                )"""
            cursor = conn.cursor()
            cursor.execute(sql, (data["OLT_NAME"], data["PON"], data["DBM_AVERAGE"]))
            conn.commit()
            cursor.close()
            
        else:
            return "Error: Banco de dados não conectado."
        