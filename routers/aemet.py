import datetime
import http.client
import json
from fastapi import APIRouter
import pytz
from urllib.request import urlopen
from models.customJson import CustomJson
from models.aemet import MeteoParams, meteo_station_id

router = APIRouter()
conn = http.client.HTTPSConnection("opendata.aemet.es")

headers = {
    'cache-control': "no-cache"
    }

@router.post("/aemet")
def get_aemet_data(params: MeteoParams):
    url = f"/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/?api_key={params.APIKey}"
    conn.request("GET", url, headers=headers)
    #conn.request("GET", "/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/?api_key=jyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqbW9udGVyb2dAYWVtZXQuZXMiLCJqdGkiOiI3NDRiYmVhMy02NDEyLTQxYWMtYmYzOC01MjhlZWJlM2FhMWEiLCJleHAiOjE0NzUwNTg3ODcsImlzcyI6IkFFTUVUIiwiaWF0IjoxNDc0NjI2Nzg3LCJ1c2VySWQiOiI3NDRiYmVhMy02NDEyLTQxYWMtYmYzOC01MjhlZWJlM2FhMWEiLCJyb2xlIjoiIn0.xh3LstTlsP9h5cxz3TLmYF4uJwhOKzA0B6-vH8lPGGw", headers=headers)
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
    f = urlopen(link)
    myfile = f.read()
    print(myfile)
    original_data = json.loads(myfile)
    #Some function for aggregation depending on the "Time_Agg" parameter should be added here
    #The Datetime field should be changed back to CET/CEST
    new_data = []
    for od in original_data:
        new_data.append(CustomJson(od))
    resultado = data
    if (new_data):
        resultado = json.dumps(new_data, indent=4)
    return resultado
