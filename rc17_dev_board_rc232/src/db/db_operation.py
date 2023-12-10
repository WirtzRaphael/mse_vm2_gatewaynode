import sqlite3
from sqlite3 import Error

SQL_CREATE_SENSORNODES_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes (
                                    id integer PRIMARY KEY,
                                    pico_id integer,
                                    radio_id integer
                                ); """
                                
SQL_CREATE_GATEWAYNODE_TABLE = """ CREATE TABLE IF NOT EXISTS gatewaynode (
                                    id integer PRIMARY KEY,
                                    radio_id integer                                    
                                ); """

SQL_CREATE_TEMPERATURE_1_TABLE = """ CREATE TABLE IF NOT EXISTS temperature_1 (
                                    id integer PRIMARY KEY,
                                    time_rtc integer NOT NULL,
                                    measure_id integer NOT NULL,
                                    temperature real NOT NULL
                                ); """

SQL_CREATE_TEMPERATURE_2_TABLE = """ CREATE TABLE IF NOT EXISTS temperature_2 (
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

def insert_temperature_into_temperature2(connection, temperature):
    sql = ''' INSERT INTO temperature_2(time_rtc, measure_id, temperature)
              VALUES(?,?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, temperature)
    
    connection.commit()
    
    return cursor.lastrowid