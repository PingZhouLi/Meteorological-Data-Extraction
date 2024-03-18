import datetime
import json

import pytz

class CustomJson(dict):
    def __init__(self, data):
        super().__init__()
        self["Station"] = data["nombre"]
        self["Datetime"] = data["fhora"]
        self["Temperature (ºC)"] = data["temp"]
        self["Pressure (hpa)"] = data["pres"]
        self["Speed (m/s)"] = data["vel"]
