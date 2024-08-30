from ._table_bases import Base
from .fork import Fork
from .seatpost import SeatPost
from .saddle import Saddle
from .stem import Stem

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import (
    Any, 
    Annotated,
    Callable,
    List
    )

# type annotations, not necessary, but nice to have:
float_2 =  Annotated[float, 2]
str_40 = Annotated[str, 40]
str_20 = Annotated[str, 20]
str_10 = Annotated[str, 10]
year = Annotated[int, 4]

class Frame(Base):
    __tablename__ = "frame"

    # Basic attributes
    serial: Mapped[str_20] = mapped_column(primary_key=True)
    serial_location: Mapped[str_20]
    brand: Mapped[str_20]
    model_year: Mapped[int]
    model_name: Mapped[str_20]
    
    material_manufacturer: Mapped[str_20]
    material_tier: Mapped[str_20]
    dropout_manufacturer: Mapped[str_20]
    dropout_type: Mapped[str_20]
    dropout_model: Mapped[str_20]
    lug_manufacturer: Mapped[str_20]
    lug_set: Mapped[str_20]
    braze_ons: Mapped[dict[str, Any]]

    # Measurements
    seat_tube_c2c_cm: Mapped[float_2]
    seat_tube_diameter_mm: Mapped[float_2]
    seat_tube_int_diameter_mm: Mapped[float_2]
    seat_tube_wall_thickness: Mapped[list[float_2]]
    seat_tube_features: Mapped[dict[str, Any]]

    top_tube_c2c_cm: Mapped[float_2]
    top_tube_diameter_mm: Mapped[float_2]
    top_tube_wall_thickness: Mapped[list[float_2]]
    top_tube_features: Mapped[dict[str, Any]]

    head_tube_c2c_cm: Mapped[float_2]
    head_tube_diameter_mm: Mapped[float_2]
    head_tube_int_diamaeter_mm: Mapped[float_2]
    head_tube_wall_thickness: Mapped[list[float_2]]
    head_tube_features: Mapped[dict[str, Any]]

    down_tube_c2c_cm: Mapped[float_2]
    down_tube_diameter_mm: Mapped[float_2]
    down_tube_wall_thickness: Mapped[list[float_2]]
    down_tube_features: Mapped[dict[str, Any]]

    seat_stays_e2e_cm: Mapped[float_2]
    seat_stay_diameter_mm: Mapped[float_2]
    seat_stay_wall_thickness: Mapped[list[float_2]]
    seat_stay_features: Mapped[dict[str, Any]]

    chain_stays_e2e_cm: Mapped[float_2]
    chain_stay_diameter_mm: Mapped[float_2]
    chain_stay_wall_thickness: Mapped[list[float_2]]
    chain_stay_features: Mapped[dict[str, Any]]

    fork: Mapped['Fork'] = relationship(back_populates='frame')
    seatpost: Mapped['SeatPost'] = relationship(back_populates='frame')
    saddle: Mapped['Saddle'] = relationship(back_populates='frame')
    stem: Mapped['Stem'] = relationship(back_populates='frame')
