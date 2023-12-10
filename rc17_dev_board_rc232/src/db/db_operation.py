import sqlite3
from sqlite3 import Error

sql_create_temperature_1_table = """ CREATE TABLE IF NOT EXISTS temperature_1 (
                                    id integer PRIMARY KEY,
                                    time_rtc integer NOT NULL,
                                    measure_id integer NOT NULL,
                                    temperature real NOT NULL
                                ); """


def insert_temperature_into_temperature1(connection, temperature):
    sql = ''' INSERT INTO temperature_1(time_rtc, measure_id, temperature)
              VALUES(?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, temperature)
    
    connection.commit()
    
    return cursor.lastrowid

