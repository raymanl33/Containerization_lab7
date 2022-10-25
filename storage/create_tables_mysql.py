import mysql.connector


db_conn = mysql.connector.connect(host="kafka.canadacentral.cloudapp.azure.com", user="user",
password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
CREATE TABLE book_tennis_court
(id INT NOT NULL AUTO_INCREMENT,
member_id VARCHAR(250) NOT NULL,
court_num INTEGER NOT NULL,
member_name VARCHAR(250) NOT NULL,
book_date VARCHAR(100) NOT NULL,
timestamp VARCHAR(100) NOT NULL,
date_created VARCHAR(100) NOT NULL,
trace_id VARCHAR(100) NOT NULL,
CONSTRAINT book_tennis_court_pk PRIMARY KEY (id))
''')
db_cursor.execute('''
CREATE TABLE book_tennis_lesson
(id INT NOT NULL AUTO_INCREMENT,
member_id VARCHAR(250) NOT NULL,
lesson_date VARCHAR(100) NOT NULL,
member_name VARCHAR(250) NOT NULL,
coach_name VARCHAR(250) NOT NULL,
lesson_rate DECIMAL NOT NULL,
timestamp VARCHAR(100) NOT NULL,
date_created VARCHAR(100) NOT NULL,
trace_id VARCHAR(100) NOT NULL,
CONSTRAINT book_tennis_lesson_pk PRIMARY KEY (id))
''')
db_conn.commit()
db_conn.close()

