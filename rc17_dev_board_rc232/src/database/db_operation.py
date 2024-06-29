import sqlite3
import pandas as pd
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
        sql = ''' INSERT INTO sensornodes_measurements(node_id, time_unix_s, sensortype, sensor_value)
        VALUES(?,?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(sql, measurements)
        
        connection.commit()
        
        return cursor.lastrowid
    
    except Error as e:
        print(f"Error: {e}")
        return None

""" Read temperatures from measurements
"""
def read_temperature_from_measurements(connection, node_id, limit):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sensornodes_measurements WHERE node_id=?", (node_id,))
        #cursor.execute("SELECT * FROM sensornodes_measurements WHERE node_id=? LIMIT ?", (node_id, limit))
        
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)

        return rows
        
    except Error as e:
        print(f"Error: {e}")
        return None

""" Read temperatures from measurements as a pandas dataframe
"""
def read_temperature_df_from_measurements(engine, node_id, limit):
    try:
        query = f'''
        SELECT * FROM sensornodes_measurements
        WHERE node_id={node_id}
        LIMIT {limit} 
        '''

        return pd.read_sql(query, engine)
        
    except Error as e:
        print(f"Error: {e}")
        return None