"""
"""
from datetime import datetime
import json
from typing import List

from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

class ForecastEntry(BaseModel):
    hour: int = Field(..., description='Hour of the day')
    temperatore: float = Field(..., description="Temperature in celcius")
    rain_chance: float = Field(..., description="Chance of rain, range 0-100%")
    humidity: int = Field(..., description="Humidity in %")
    wind_direction: str = Field(..., direction = "N | S | E | W")
    wind_speed_kmh: int = Field(..., description="Wind speed km/h")

class Forecast(BaseModel):
    lat: float = Field(..., description="lat")
    lon: float = Field(..., description="lon")
    forecast: List[ForecastEntry]

class MowerSchedule(BaseModel):
    start: int = Field(..., description="Start time in minutes since midnight")
    duration: int = Field(..., description="Activity in minutes")
    reason: str = Field(..., direction = "Reasoning behind the decision")



class MowerDataEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, Forecast) or isinstance(o, ForecastEntry) or isinstance(o, MowerSchedule):
            return o.__dict__
        return json.JSONEncoder.default(self, o)

class LLMWrapper():

    def __init__(self):
        model = "gpt-3.5-turbo-0125"
        self.llm = ChatOpenAI(model=model)

    async def get_forecast(self, lat: float, lon: float, date: datetime) -> Forecast:
        latlon = f"{lat},{lon}"
        date_str = date.strftime('%Y-%m-%d')

        query = f"Get weather forecast for {date_str} at {latlon} for full day, hourly intervals."
        tools = [Forecast]
        bind_tools = self.llm.bind_tools(tools)
        chain = bind_tools | PydanticToolsParser(tools=tools)
        ret = chain.invoke(query)
        return ret[0]

    async def create_schedule(self, forecast: Forecast) -> MowerSchedule:
        query = '''
    Based on the specified forecast try to establish the best schedule
    for automatic mower. Schedule API allows to only specify start time
    and duration of activity in minutes. There can be many entries but
    minimal duration should be 30minutes.
    sFind the best periods, preferably during the day with
    best weather conditions for mowing. If the conditions do not allow
    for mowing return an empty list.
    The area to cover is roughly 200m2 and the mower works for everyday.
    Add detailed reason to justify the decision, include what weather
    parameters affected this result. The forecast is:
    '''
        for f in forecast.forecast:
            v = vars(f)
            v['hour'] = f'{v["hour"]:02d}:00'
            query += f'- {json.dumps(v)}\n'

        tools = [MowerSchedule]
        bind_tools = self.llm.bind_tools(tools)
        chain = bind_tools | PydanticToolsParser(tools=tools)

        ret = chain.invoke(query)
        return ret
