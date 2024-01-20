from datetime import datetime, timedelta
import influxdb_client
import pandas as pd
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Flask, render_template, jsonify
import json

# Konfiguracja InfluxDB
influxdb_host = "127.0.0.1:8086"
bucket = "admin"
org = "c9d2f82bec384031"
token = "YY7AtGmBB5uAAcgdEP5G0u34dqbbmEYmr7-ZgOEG4spK_6l9XMThk7HQckSQVWwD7mGxKSLzcTqHXU8bGU5pow=="

app = Flask(__name__)

@app.route('/<weaponType>/<skinName>')
def index(weaponType, skinName):
    # Tutaj możesz użyć wartości weaponType i skinName
    # do przekazania ich do funkcji get_data() lub wykonywania innych operacji

    getchart = get_data(weaponType, skinName)

    context = {'getchart': getchart}
    return render_template('skin.html', **context)

@app.route('/get_data', methods=['GET'])
def get_data(weaponType,skinName):

    client = influxdb_client.InfluxDBClient(
        url=influxdb_host,
        token=token,
        org=org
    )
    
    datax = []
    datay = []
    
    for x in range(30, 0, -1):
        if x == 1:
            query = f'''
            from(bucket: "admin")
            |> range(start: -{x}d, stop: now())
            |> filter(fn: (r) => r["_measurement"] == "{weaponType}")
            |> filter(fn: (r) => r["Normal"] == "{skinName}")
            |> filter(fn: (r) => r["_field"] == "Cena")
         '''
        else:
            query = f'''
            from(bucket: "admin")
            |> range(start: -{x}d, stop: -{x-1}d)
            |> filter(fn: (r) => r["_measurement"] == "{weaponType}")
            |> filter(fn: (r) => r["Normal"] == "{skinName}")
            |> filter(fn: (r) => r["_field"] == "Cena")
         '''
        
        query_api = client.query_api()
        result = query_api.query(query, org=org)

        for table in result:
            for record in table.records:
                value = record.get_value()
                time = record.get_time()
                datax.append(time)
                datay.append(value)

    
    df = pd.DataFrame({'time': datax, 'value': datay})
    #return jsonify(df.to_dict()) # zwróć dane jako JSON
    # Konwertowanie ramki danych do formatu JSON
    json_data = df.to_json(orient='records')

    # Wyświetlenie wyniku
    json_data = json.loads(json_data)
    new_json_data = json.dumps([[entry["time"], entry["value"]] for entry in json_data], indent=4)
    return(new_json_data)

if __name__ == '__main__':
#print(get_data())
    pass

app.run()