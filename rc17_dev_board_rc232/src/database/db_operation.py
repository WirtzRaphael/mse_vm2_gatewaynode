import sqlite3
from sqlite3 import Error

SQL_CREATE_SENSORNODES_INFO_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_info (
                                    id integer PRIMARY KEY,
                                    time_utc integer NOT NULL,
                                    node_id integer NOT NULL,
                                    pico_id integer NOT NULL,
                                    radio_id integer
                                ); """
                                
SQL_CREATE_GATEWAYNODE_TABLE = """ CREATE TABLE IF NOT EXISTS gatewaynode (
                                    id integer PRIMARY KEY,
                                    radio_id integer                                    
                                ); """
               
SQL_CREATE_SENSORNODES_SENSORS_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_sensors (
                                    id integer PRIMARY KEY,
                                    node_id integer NOT NULL,
                                    sensor_id integer
                                ); """
                                
SQL_CREATE_SENSORNODES_SENSORS_DATA_TABLE = """ CREATE TABLE IF NOT EXISTS sensornodes_sensor_data (
                                    id integer PRIMARY KEY,
                                    time_receive_utc integer NOT NULL,
                                    time_rtc integer NOT NULL,
                                    measure_nr integer NOT NULL,
                                    sensornode_id integer NOT NULL,
                                    sensor_id integer NOT NULL,
                                    sensor_value real NOT NULL
                                ); """

def insert_temperature_into_sensor_data(connection, sensor_data):
    try:
        sql = ''' INSERT INTO sensornodes_sensor_data(time_receive_utc, time_rtc, measure_nr, sensornode_id, sensor_id, sensor_value)
                VALUES(?,?,?,?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(sql, sensor_data)
        
        connection.commit()
        
        return cursor.lastrowid
    
    except Error as e:
        return None
