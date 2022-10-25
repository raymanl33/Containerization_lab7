import mysql.connector




db_conn = mysql.connector.connect(host="kafka.canadacentral.cloudapp.azure.com", user="user",
password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
DROP TABLE book_tennis_court, book_tennis_lesson
''')


db_conn.commit()
db_conn.close()