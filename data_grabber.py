# imports
import sys
from influxdb import InfluxDBClient as db
from datetime import datetime
from sensors import *
import urllib3
import xmltodict

# A variable for debug output
debug = True;

# influx
host = "localhost"
port = "8086"
user = "pi"
password = "rpi"
dbname = "heizungsdaten"
client = db(host, port, user, password, dbname)

# urllib3
http = urllib3.PoolManager()

# IP-adresses to get data
menu_url = 'http://192.168.178.80:8080/user/menu'
url_to_append = 'http://192.168.178.80:8080/user/var/'


# important functions, use should be obvious by name
def get_name_and_uri_by_index(index):
    return sensors[index]

def get_single_sensor_value_and_unit_from_uri(sensor_uri):
    url = url_to_append + sensor_uri
    xml = http.request('GET', url)

    data = xmltodict.parse(xml.data)
    value = data['eta']['value']['@strValue']
    unit = data['eta']['value']['@unit']

    if ',' in value:
        value = value.replace(',', '.')
    if 'x' in value:
        value = sys.float_info.max
    return (float(value), unit)

def read_all_sensors():
    pass

def append_to_values_dictionary():
    for index, value in enumerate(sensors):
        key, _ = value
        if values[index] != sys.float_info.max:
            values_dictionary.update({key: values[index]})
        else:
            print('No valid value at index ' + str(index) + ' (Sensor: "%s")' % (key))


def send_to_db(data):
    client.write_points(data)

def create_and_send_json_dictionary(dictionary_in): # {'sensor0':value0, 'sensor1':value1}
    now = datetime.now()
    iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    local_dict = [
        {
            "measurement": "etaheizung",
            "tags": {
                "user": "raspi"
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

if __name__ == '__main__':
    for i in range(len(sensors)):
        name, uri = get_name_and_uri_by_index(i)
        value, unit = get_single_sensor_value_and_unit_from_uri(uri)
        values.append(value)
        print(name + ": " + str(value) + " " + unit)
    append_to_values_dictionary()
    create_and_send_json_dictionary(values_dictionary)