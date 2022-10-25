import sqlite3

conn = sqlite3.connect('tennis_booking.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE book_tennis_court
          (id INTEGER PRIMARY KEY ASC, 
           member_id VARCHAR(250) NOT NULL,
           court_num INTEGER NOT NULL,
           member_name VARCHAR(250) NOT NULL,
           book_date VARCHAR(100) NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE book_tennis_lesson
          (id INTEGER PRIMARY KEY ASC, 
           member_id VARCHAR(250) NOT NULL,
           lesson_date VARCHAR(100) NOT NULL,
           member_name VARCHAR(250) NOT NULL,
           coach_name VARCHAR(250) NOT NULL,
           lesson_rate DECIMAL NOT NULL,
           timestamp VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
