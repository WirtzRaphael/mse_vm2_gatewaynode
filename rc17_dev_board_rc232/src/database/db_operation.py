import sqlite3
from sqlite3 import Error

SQL_CREATE_SENSORNODES_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_info (
                                    id integer PRIMARY KEY,
                                    time_unix_s integer NOT NULL,
                                    node_id integer NOT NULL,
                                    pico_id integer NOT NULL,
                                    firmware_version integer NOT NULL
                                ); """
               
SQL_CREATE_SENSORNODES_SENSORS_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_sensors (
                                    id integer PRIMARY KEY,
                                    node_id integer NOT NULL,
                                    sensor_id integer
                                ); """
                                
SQL_CREATE_SENSORNODES_MEASUREMENTS_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_measurements (
                                    id integer PRIMARY KEY,
                                    node_id integer NOT NULL,
                                    time_unix_s integer NOT NULL,
                                    sensortype integer NOT NULL,
                                    sensor_value real NOT NULL
                                ); """

def insert_temperature_into_measurements(connection, measurements):
    try:
        sql = ''' INSERT INTO sensornodes_measurements(node_id, time_unix_s, sensortype, sensor_value
        VALUES(?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(sql, measurements)
        
        connection.commit()
        
        return cursor.lastrowid
    
    except Error as e:
        return None
