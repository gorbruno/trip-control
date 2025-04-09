from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
import datetime

class DayDTO(BaseModel):
    date: Optional[datetime.datetime] = Field(default=None)
    refill: Optional[float] = Field(default=None)
    fuel_start: Optional[float] = Field(default=None)
    fuel_end: Optional[float] = Field(default=None)
    odometer_start: Optional[int] = Field(default=None)
    odometer_end: Optional[int] = Field(default=None)
    mileage: Optional[int] = Field(default=None)
    consumption: Optional[float] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

class CoordinatesDTO(BaseModel):
    lat: Optional[float] = Field(default=None)
    lon: Optional[float] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)

class LocationDTO(BaseModel):
    name: Optional[str] = Field(default=None)
    coords: Optional[CoordinatesDTO] = Field(default=None)
    additional_name: Optional[str] = Field(default=None)
    comment_name: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    housenum: Optional[str | int] = Field(default=None)
    address: Optional[str] = Field(default=None)
    additional_address: Optional[str] = Field(default=None)
    comment_address: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    country_a: Optional[str] = Field(default=None)
    region: Optional[str] = Field(default=None)
    region_a: Optional[str] = Field(default=None)
    county: Optional[str] = Field(default=None)
    locality: Optional[str] = Field(default=None)
    wof_country: Optional[int] = Field(default=None)
    wof_region: Optional[int] = Field(default=None)
    wof_county: Optional[int] = Field(default=None)
    wof_locality: Optional[int] = Field(default=None)
    
    model_config = ConfigDict(from_attributes=True)

class TaskDTO(BaseModel):
    day: Optional[DayDTO] = Field(default=None)
    task_name: Optional[str] = Field(default=None)
    location: Optional[LocationDTO] = Field(default=None)
    department: Optional[str] = Field(default=None)
    responsible: Optional[str] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)

class DistanceDTO(BaseModel):
    day: Optional[DayDTO] = Field(default=None)
    location_from: Optional[LocationDTO] = Field(default=None)
    location_to: Optional[LocationDTO] = Field(default=None)
    distance: Optional[int] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)