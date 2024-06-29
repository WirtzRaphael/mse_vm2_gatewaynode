import sqlite3
from sqlite3 import Error

SQL_CREATE_SENSORNODES_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_info (
                                    id integer PRIMARY KEY,
                                    time_unix_s integer NOT NULL,
                                    node_id integer NOT NULL,
                                    pico_id integer NOT NULL,
                                    firmware_version integer NOT NULL,
                                    radio_id integer
                                ); """
               
SQL_CREATE_SENSORNODES_SENSORS_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_sensors (
                                    id integer PRIMARY KEY,
                                    node_id integer NOT NULL,
                                    sensor_id integer
                                ); """
                                
SQL_CREATE_SENSORNODES_MEASUREMENTS_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_sensor_data (
                                    id integer PRIMARY KEY,
                                    time_unix_s integer NOT NULL,
                                    sensortype integer NOT NULL,
                                    sensor_value real NOT NULL,
                                    signal_strength integer
                                ); """

def insert_temperature_into_sensor_data(connection, sensor_data):
    try:
        sql = ''' INSERT INTO sensornodes_sensor_data(time_receive_unix_s, time_rtc_s, measure_nr, sensornode_id, sensor_id, sensor_value, signal_strength)
                VALUES(?,?,?,?,?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(sql, sensor_data)
        
        connection.commit()
        
        return cursor.lastrowid
    
    except Error as e:
        return None
