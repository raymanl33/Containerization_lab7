import sqlite3

conn = sqlite3.connect('stats.sqlite')


c = conn.cursor()
c.execute('''
        CREATE TABLE stats
        (id INTEGER PRIMARY KEY ASC,
        num_court_bookings INTEGER NOT NULL,
        max_court_bookings INTEGER NOT NULL,
        num_lesson_bookings INTEGER NOT NULL,
        max_lesson_bookings INTEGER NOT NULL,
        last_updated VARCHR(100) NOT NULL)
        ''' )

conn.commit()
conn.close()