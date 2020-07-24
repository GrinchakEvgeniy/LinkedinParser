import sqlite3
class DB:
    # this class create, insert, drop and select database
    def main(self,list_value):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE albums
	                  (Company_name text, Company_discription text, address text,
	                   URL text, Contact1 text, Title1 text, Phone1 text, Email1 text,
	                   Contact2 text, Title2 text, Phone2 text, Email2 text,
	                   Contact3 text, Title3 text, Phone3 text, Email3 text,
	                   Contact4 text, Title4 text, Phone4 text, Email4 text)
	               """)
        except:
            pass
        try:
            # create data after screpping site
            if len(list_value) == 16:
                fields = [(list_value[0], list_value[1], list_value[2], list_value[3], list_value[4], list_value[5],
                           list_value[6], list_value[7], list_value[8], list_value[9], list_value[10], list_value[11],
                           list_value[12], list_value[13], list_value[14], list_value[15], 'Not found', 'Not found', 'Not found',
                           'Not found')]
                cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", fields)
                conn.commit()
            elif len(list_value) == 12:
                fields = [(list_value[0], list_value[1], list_value[2], list_value[3], list_value[4], list_value[5],
                           list_value[6], list_value[7], list_value[8], list_value[9], list_value[10], list_value[11],
                           'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found')]
                cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", fields)
                conn.commit()
            elif len(list_value) == 8:
                fields = [(list_value[0], list_value[1], list_value[2], list_value[3], list_value[4], list_value[5],
                           list_value[6], list_value[7], 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found', 'Not found',
                           'Not found', 'Not found', 'Not found', 'Not found')]
                cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", fields)
                conn.commit()
            else:
                fields = [(list_value[0], list_value[1], list_value[2], list_value[3], list_value[4], list_value[5],
                           list_value[6], list_value[7], list_value[8], list_value[9], list_value[10], list_value[11],
                           list_value[12], list_value[13], list_value[14], list_value[15], list_value[16],
                           list_value[17], list_value[18], list_value[19])]
                cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", fields)
                conn.commit()
        except:
            pass
        cursor.close()

    def clear(self):
        # delete table\command clear
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS albums")
        cursor.close()

    def select(self):
        # select data in database and save her in array post
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        try:
            sql = "SELECT * FROM albums"
            cursor.execute(sql)
            list_ret = cursor.fetchall()  # or use fetchone
            return list_ret
        except:
            pass
        cursor.close()

    def delete(self, value):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        sql = "DELETE FROM albums WHERE Company_name = ? "
        cursor.execute(sql, (value,))
        conn.commit()
        cursor.close()