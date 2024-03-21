from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum
import datetime
import pytz 

def meteo_station_id(argument):
    match argument:
        case "Meteo Station Gabriel de Castilla":
            return 89070
        case "Meteo Station Juan Carlos I":
            return 89064
        case default:
            return 89070
        
def getTimeAggEquivalent(argument: str):
    match argument:
        case 'None':
            return None
        case "Hourly":
            return 'h'
        case "Daily":
            return 'D'
        case "Monthly":
            return 'ME'
        case default:
            return None        

class MeteoParams(BaseModel):
    APIKey: str = Field(default='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwaW5nMjQyODdAZ21haWwuY29tIiwianRpIjoiMDA2NDNiMTktODFiMi00NTFiLWFjNmItOTI1MjJiNDljZjQ4IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3MTA3ODk3OTEsInVzZXJJZCI6IjAwNjQzYjE5LTgxYjItNDUxYi1hYzZiLTkyNTIyYjQ5Y2Y0OCIsInJvbGUiOiIifQ.IlbV3fwlfIY22Ew5eIg04usQvAuZfZJuAGAIP9IxcNk')
    dateTimeStart: datetime.datetime = Field(default=datetime.datetime(2022, 3, 24))
    dateTimeEnd: datetime.datetime = Field(default=datetime.datetime(2022, 7, 24))
    Meteo_Measurement_Station: Literal["Meteo Station Juan Carlos I","Meteo Station Gabriel de Castilla"]
    Time_Agg: Literal["None", "Hourly", "Daily", "Monthly"]


