# imports
from influxdb import InfluxDBClient as db
from datetime import datetime
import sensors

# A variable for debug output
debug = True;

# influx
host = "localhost"
port = "8086"
user = "pi"
password = "rpi"
dbname = "heizungsdaten"
client = db(host, port, user, password, dbname)

# IP-adresses to get data
menu_url = 'http://192.168.178.80:8080/user/menu'
url_to_append = 'http://192.168.178.80:8080/user/var/'


# important functions, use should be obvious by name
def get_name_and_uri_by_index(index):
    pass

def get_single_sensor_data_from_uri(sensor_uri):
    pass

def read_all_sensors():
    pass

def append_to_values_dictionary(x):
    for index, key in enumerate(sensors):
        values_dictionary.update({key: values[index]})

def send_to_db(data):
    client.write_points(data)

def create_and_send_json_dictionary(dictionary_in): # {'sensor0':value0, 'sensor1':value1}
    now = datetime.now()
    iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    local_dict = [
        {
            "measurement": "eta-heizung",
            "tags": {
                "user": "rpi"
            },
            "time": iso,
            "fields": dictionary_in
        }
    ]
    if debug:
        print("Dictionary sent to database:\n%s"%(local_dict))
        print(iso)

    send_to_db(local_dict)

values_dictionary = {}
values = []

try:
    read_all_sensors()
    append_to_values_dictionary()
    create_and_send_json_dictionary(values_dictionary)
except KeyboardInterrupt:
    print("Inerrupted")
except Exception as e:
    print(e)
