import pandas as pd
import datetime
import http.client
import json
from fastapi import APIRouter
import pytz
from urllib.request import urlopen
from models.customJson import CustomJson
from models.aemet import MeteoParams, getTimeAggEquivalent, meteo_station_id


router = APIRouter()
conn = http.client.HTTPSConnection("opendata.aemet.es")

headers = {
    'cache-control': "no-cache"
    }

@router.post("/aemet")
def get_aemet_data(params: MeteoParams):
    url = f"/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/?api_key={params.APIKey}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return list(data)

@router.post("/antartida")
def get_aemet_data(params: MeteoParams):
    id_station = meteo_station_id(params.Meteo_Measurement_Station)
    fechaIni = params.dateTimeStart.strftime("%Y-%m-%dT%H:%M:%SUTC").replace(':','%3A')
    fechaFin = params.dateTimeEnd.strftime("%Y-%m-%dT%H:%M:%SUTC").replace(':','%3A')
    url = f"/opendata/api/antartida/datos/fechaini/{fechaIni}/fechafin/{fechaFin}/estacion/{id_station}"
    headers = {
    'cache-control': "no-cache",
    'Api_key': params.APIKey
    }
    conn.request("GET", url, headers=headers)
    #https://opendata.aemet.es/opendata/api/antartida/datos/fechaini/2022-03-24T00%3A00%3A00UTC/fechafin/2022-07-24T00%3A00%3A00UTC/estacion/89064

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    data_web = json.loads(data.decode("utf-8"))
    #The expected data is generated inside a new link
    link = data_web['datos']

    transformed_data = getAggregatedData(link, params.Time_Agg)
    #The result is displayed at the Terminal
    print('The solution is: ')
    print(transformed_data)
    result = data
    if (transformed_data.any):
        result = transformed_data.to_json(orient='records', date_format='iso')
    return result

def getAggregatedData(link: str, granularity: str):
    #We open the link provided to get the data
    f = urlopen(link)
    myfile = f.read()
    original_data = json.loads(myfile)
    ##The Datetime field should be changed back to CET/CEST
    ##Convert the array of objects into a DataFrame with the specified property names for pandas aggrupation functions
    # ["Station"] <= ["nombre"]
    # ["Datetime"] <= ["fhora"]
    # ["Temperature (ºC)"] <= ["temp"]
    # ["Pressure (hpa)"] <= ["pres"]
    # ["Speed (m/s)"] <= ["vel"]
    df = pd.DataFrame([{'Station': d['nombre'],'Datetime': d['fhora'], 'Temperature (ºC)': d['temp'], 'Pressure (hpa)': d['pres'], 'Speed (m/s)': d['vel']} for d in original_data])

    timeAgg = getTimeAggEquivalent(granularity)

    if (timeAgg):
        #Set the datetime column as the index
        df['Datetime'] = pd.to_datetime(df["Datetime"])
        #A guess is made that the datetime provided by the server is in UTC, so we convert it to Europe/Madrid as requested 
        df['Datetime'] = pd.to_datetime(df["Datetime"]).dt.tz_localize('UTC').dt.tz_convert('Europe/Madrid')
        df.set_index('Datetime', inplace=True)
        #The output dataset shall be aggregated based on the user selection of the Time Aggregation field. It's strange that it's required aggregation instead of averaging
        new_data = df.groupby('Station').resample(timeAgg).agg({'Temperature (ºC)':'sum','Pressure (hpa)':'sum','Speed (m/s)':'sum'}).reset_index()
    else:
        new_data = df

    return new_data