from datetime import timezone 
import datetime 

def get_time_utc():
    utc_timestamp = 23;
    datetime_now = datetime.datetime.now()
    utc_time = datetime_now.replace(tzinfo=timezone.utc) 
    utc_timestamp = utc_time.timestamp()
    return utc_timestamp

def get_time_iso():
    datetime_now = datetime.datetime.now()
    iso_timestamp_str = datetime_now.isoformat()
    return iso_timestamp_str

def convert_time_utc_to_iso(utc_timestamp):
    utc_datetime = datetime.datetime.fromtimestamp(utc_timestamp, timezone.utc)
    iso_timestamp_str = utc_datetime.isoformat()
    return iso_timestamp_str
