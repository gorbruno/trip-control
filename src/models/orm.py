from sqlalchemy import (
    Column, Integer, Float, String, Date, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

# 1. Make calls for async attrs possible with AsyncAttrs
# 2. Base class override with DTO-like init
# This custom __init__ allows passing nested dicts or lists of dicts
# to auto-instantiate relationships and column values.
class Base(AsyncAttrs, DeclarativeBase):
    def __init__(self, **kw):
        cls = self.__class__
        mapper = cls.__mapper__

        for key in kw:
            if key in mapper.relationships:
                related_class = mapper.relationships[key].entity.class_
                value = kw[key]
                if isinstance(value, dict):
                    setattr(self, key, related_class(**value))
                elif isinstance(value, list):
                    setattr(
                        self, 
                        key, 
                        [related_class(**v) if isinstance(v, dict) else v for v in value]
                    )                
                else:
                    setattr(self, key, value)
            elif key in mapper.columns.keys():
                setattr(self, key, kw[key])
            else:
                print(f"WARNING: Invalid keyword argument: {key}")

class DayORM(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False)
    refill = Column(Float, nullable=True)
    fuel_start = Column(Float, nullable=False)
    fuel_end = Column(Float, nullable=False)
    odometer_start = Column(Integer, nullable=False)
    odometer_end = Column(Integer, nullable=False)

    # Task links
    tasks = relationship("TaskORM", back_populates="day", cascade="all, delete-orphan")

    @property
    def mileage(self) -> int:
        if self.odometer_start is not None and self.odometer_end is not None:
            return self.odometer_end - self.odometer_start 
        return None

    @property
    def consumption(self) -> float:  # Fuel consumption
        if self.mileage:
            return self.mileage * 19.35 / 100
        return None

class CoordinateORM(Base):
    __tablename__ = 'coordinates'

    id = Column(Integer, primary_key=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    __table_args__ = (UniqueConstraint('lat', 'lon', name='unique_coordinates'),)

    def __repr__(self):
        return f"<Coordinates(id={self.id}, lat={self.lat}, lon={self.lon})>"


class LocationORM(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    additional_name = Column(String, nullable=True)
    comment_name = Column(String, nullable=True)
    street = Column(String, nullable=False)
    housenum = Column(String, nullable=False)
    additional_address = Column(String, nullable=True)
    comment_address = Column(String, nullable=True)
    country = Column(String, nullable=False)
    country_a = Column(String, nullable=False)
    region = Column(String, nullable=False)
    region_a = Column(String, nullable=False)
    county = Column(String, nullable=True)
    locality = Column(String, nullable=True)
    wof_country = Column(Integer, nullable=False)
    wof_region = Column(Integer, nullable=False)
    wof_county = Column(Integer, nullable=True)
    wof_locality = Column(Integer, nullable=True)
    
    coords_id = Column(Integer, ForeignKey('coordinates.id'))
    coords = relationship('CoordinateORM', backref='locations')

    @property
    def address(self) -> str:
        parts = [
            self.name or "",
            f"({self.comment_name})" if self.comment_name else "",
            f"{', ' if self.name else ''}{self.additional_name}, " if self.additional_name else "",
            f"{', ' if self.name and not self.additional_name else ''}{self.street}",
            f", {self.housenum}",
            f" - {self.additional_address}" if self.additional_address else "",
            f" ({self.comment_address})" if self.comment_address else ""
        ]
        return ''.join(parts).strip()

    def __repr__(self):
        return f"<Location(id={self.id}, name={self.name}, address={self.address}, coords={self.coords})>"

    # Task links
    tasks = relationship("TaskORM", back_populates="location", cascade="all, delete-orphan")
    # Distance links
    dist_from = relationship("DistanceORM", foreign_keys="[DistanceORM.loc_from]", back_populates="loc_from_obj", cascade="all, delete-orphan")
    dist_to = relationship("DistanceORM", foreign_keys="[DistanceORM.loc_to]", back_populates="loc_to_obj", cascade="all, delete-orphan")

class TaskORM(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)
    count = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    loc_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    department = Column(String, nullable=False)
    responsible = Column(String, nullable=False)
    note = Column(String, nullable=True)

    def __repr__(self):
        return f"<Task(id={self.id}, day_id={self.day_id}, name={self.name}, department={self.department}, responsible={self.responsible})>"

    # Links
    day = relationship("DayORM", back_populates="tasks")
    location = relationship("LocationORM", back_populates="tasks")

class DistanceORM(Base):
    __tablename__ = "distances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    loc_from = Column(Integer, ForeignKey("locations.id"), nullable=False)  # Start point
    loc_to = Column(Integer, ForeignKey("locations.id"), nullable=False)  # End point
    distance = Column(Integer, nullable=False)

    # Links
    loc_from_obj = relationship("LocationORM", foreign_keys=[loc_from], back_populates="dist_from")
    loc_to_obj = relationship("LocationORM", foreign_keys=[loc_to], back_populates="dist_to")

    def __repr__(self):
        return f"<Distance(id={self.id}, loc_from={self.loc_from}, lot_to={self.loc_to}, distance={self.distance})>"
