
from influxdb import InfluxDBClient

url = "http://localhost:8086"
host = "localhost"
port = 8086
token = "qnQFoMC9i3npWqVRFMfe1J8yldcaEYKbLENlA5qUD6Ko5EIIPW1zrgGL11b_ocfwAmOgWqLrp5LDZtbfqmISPA=="
dbname = "my-bucket"
org = "my-org"

#client = InfluxDBClient(host, port, token, org)
client = InfluxDBClient(url, token, org)

data = [
    {
        "measurement": "temperature",
        "tags": {
            "location": "office",
        },
        "fields": {
            "value": 25.5,
        }
    }
]

write_api = client.write_api()

# Write the data to InfluxDB
write_api.write(bucket, org, data)

# Close the connection
client.close()