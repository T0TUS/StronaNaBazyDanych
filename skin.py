from datetime import datetime, timedelta
import influxdb_client
import pandas as pd
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Flask, render_template, jsonify
import json
import psycopg2

# Konfiguracja InfluxDB
influxdb_host = "127.0.0.1:8086"
bucket = "admin"
org = "c9d2f82bec384031"
token = "YY7AtGmBB5uAAcgdEP5G0u34dqbbmEYmr7-ZgOEG4spK_6l9XMThk7HQckSQVWwD7mGxKSLzcTqHXU8bGU5pow=="

# PostgreSQL database configuration
db_config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'admin',
    'port': '5432'
}

app = Flask(__name__)

@app.route('/<weaponType>/<skinName>')
def skin(weaponType, skinName):
    # Tutaj możesz użyć wartości weaponType i skinName
    # do przekazania ich do funkcji get_data() lub wykonywania innych operacji

    getchart = get_data(weaponType, skinName)
    getpostgresdata = postgres_data(weaponType, skinName)

    context = {'getchart': getchart, 'getpostgresdata': getpostgresdata}
    return render_template('skin.html', **context)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/inventory')
def inventory():
    return render_template('../inventory.html')

@app.route('/')
def index():
    return render_template('index.html')


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

@app.route('/postgres_data', methods=['GET'])
def postgres_data(weaponType,skinName):
    split_text = skinName.split(" (")
    skin_name = split_text[0]
    wear_condition = split_text[1][:-1]  # Pomijamy ostatni znak, który jest nawiasem zamykającym

    # Connect to the PostgreSQL database
    conn = connect_to_postgres()
    cursor = conn.cursor()

    # Example query - replace with your own query
    query = """
    SELECT * FROM "Typ przedmiotu" 
    WHERE "Typ przedmiotu" = "{weapon_type}" AND
    "Stan zuzycia" = "{wear_condition}" AND
    "Nazwa skorki" = "{skin_name}"
    """
    cursor.execute(query,({weaponType},{wear_condition},{skin_name}))
    conn.commit()

    # Fetch all rows from the result set
    data = cursor.fetchone()

    # Close the database connection
    cursor.close()
    conn.close()

    return data

def connect_to_postgres():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="admin",
            host="localhost",
            port="5432",
            database="postgres"
        )
        return connection
    except Exception as e:
        print(f"Błąd połączenia z bazą danych: {e}")
        return None

if __name__ == '__main__':
    print(postgres_data('AWP','Asiimov (Battle-Scarred)'))
    pass

app.run()