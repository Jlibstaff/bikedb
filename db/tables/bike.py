#!/media/jll/Occam/dev/sandbox/bikedb/.venv/bin/python3

from datetime import date

from inspect import get_annotations

from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy import JSON, ARRAY
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import Any, Annotated

from jllogging import JLLogger

# type annotations, not necessary, but nice to have:
float_2 = Annotated[float, 2]
str_20 = Annotated[str, 20]
str_10 = Annotated[str, 10]
year = Annotated[int, 4]


def log_setup() -> JLLogger:
    logger = JLLogger('bike_db')
    logger.terminal_setup(10)
    logger.file_setup('bikedb.log', 10)
    return logger

logger = log_setup()

class AnnotationBase(DeclarativeBase):

    logger.debug(f'seting type annotation_map:')
    type_annotation_map = {
        str_20: String(20),
        str_10: String(10),
        float_2: Float(precision=2),
        year: Integer,
        dict[str, Any]: JSON,
        list[int]: ARRAY(Integer),
        list[str]: ARRAY(String),
        list[float_2]: ARRAY(Float)
    }    

class Base(AnnotationBase):
    def __init__(self):
        super().__init__()
    
    __abstract__ = True
    #__tablename__ = "base"

    logger.debug(f'creating default columns')
    
    production_year: Mapped[year]
    manufacturer: Mapped[str_20]
    model_name: Mapped[str_20]
    stamped_codes: Mapped[dict[str, Any]]
    style: Mapped[str_20]

    #built_weight_kg: Mapped[float_2]
    purchase_date: Mapped[date]
    purchase_price: Mapped[float_2]
    value_low_usd: Mapped[float_2]
    value_avg_usd: Mapped[float_2]
    value_high_usd: Mapped[float_2]
    
    _locals = locals()

    def _set_repr(self) -> None:
        _annotations = self.__annotations__
        _annotations.update(self._locals['__annotations__'])
        repr_head = f"<{self.__class__.__name__}("
        repr_body_list = [f'{k}={v}' for k, v in _annotations.items()]
        repr_body = ','.join(repr_body_list)
        repr_tail = ')>'
        repr = ''.join([repr_head, repr_body, repr_tail])
        return repr

    def __repr__(self):
        return self._set_repr()
    
class Frame(Base):
    def __init__(self):
        super().__init__()

    __tablename__ = "frames"

    # Basic attributes
    serial: Mapped[str_20] = mapped_column(primary_key=True)
    serial_location: Mapped[str_20]
    #stamped_codes: Mapped[dict[str, Any]]
    brand: Mapped[str_20]
    #manufacturer: Mapped[str_20]
    #production_year: Mapped[year]
    model_year: Mapped[int]
    model_name: Mapped[str_20]
    #style: Mapped[str_20]
    
    material: Mapped[str_20]
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

    weight_spec_g: Mapped[float_2]
    weight_actual_g: Mapped[float_2]

    #purchase_date: Mapped[date]
    #purchase_price: Mapped[float_2]
    
    #value_low_usd: Mapped[float_2]
    #value_avg_usd: Mapped[float_2]
    #value_high_usd: Mapped[float_2]

    def __repr__(self):
        return self._set_repr()

class Fork(Base):
    __tablename__ = "forks"

    
    #purchase_date: Mapped[date]
    #production_year: Mapped[year]
    stamped_codes: Mapped[dict[str, Any]] = mapped_column(primary_key=True)
    frame_serial: Mapped[str_20] = mapped_column(ForeignKey('frames.serial'))
    #production_year: Mapped[int]
    #manufacturer: Mapped[str_20]
    #model_name: Mapped[str_20]
    material: Mapped[str_20]
    #style: Mapped[str_20]
    
    material_tier: Mapped[str_20]
    crown_type: Mapped[str_20]
    dropout_manufacturer: Mapped[str_20]
    dropout_type: Mapped[str_20]

    steerer_length_mm: Mapped[float_2]
    threaded_length_mm: Mapped[float_2]
    blade_length_mm: Mapped[float_2]
    crown_width_mm: Mapped[float_2]
    spacing_mm: Mapped[float_2]
    
    offset_rake: Mapped[float_2]
    trail: Mapped[str_20]
    weight_g: Mapped[float_2]
    
    def __repr__(self):
        return self._set_repr()
    
# class Seatpost(Base):
#     __tablename__ = "seatposts"

#     frame_serial: Mapped[str] = self._string_primary
#     production_year: Mapped[int] = self._integer
#     manufacturer: Mapped[str] = self._string_20
#     model_name: Mapped[str] = self._string_20
#     stamped_codes: Mapped[ARRAY] = self._array
#     material: Mapped[str] = _string_10
    
#     diameter_mm: Mapped[float] = self._float_2
#     clamp_type: Mapped[str] = self._string_20
#     weight_g: Mapped[float] = self._float_2



# class Saddle(Base):
#     __tablename__ = "saddles"

#     frame_serial: Mapped[str] = self._string_20
#     production_year: Mapped[int] = self._integer
#     manufacturer: Mapped[str] = self._string_20
#     model_name: Mapped[str] = self._string_20
#     stamped_codes: Mapped[ARRAY] = self._array

#     rail_material: Mapped[str] = _string_10
#     base_material: Mapped[str] = _string_10
#     cushion_material: Mapped[str] = _string_10
#     dimensions_lwh_cm: Mapped[ARRAY] = self._array
#     weight_g: Mapped[float] = self._float_2

# class Stem(Base):
#     __tablename__ = "stems"

#     frame_serial: Mapped[str] = self._string_20
#     production_year: Mapped[int] = self._integer
#     manufacturer: Mapped[str] = self._string_20
#     model_name: Mapped[str] = self._string_20
#     stamped_codes: Mapped[ARRAY] = self._array

#     style: Mapped[str] = self._string_20
#     quill_style: Mapped[str] = self._string_20

#     height_mm: Mapped[float] = self._float_2
#     length_mm: Mapped[float] = self._float_2
#     quill_diameter_mm: Mapped[float] = self._float_2
#     steerer_diameter_mm: Mapped[float] = self._float_2
#     clamp_diameter: Mapped[float] = self._float_2
#     weight_g: Mapped[float] = self._float_2

class Bike(Base):
    def __init__(self):
        super().__init__()
    
    __tablename__ = "bikes"

    purchase_date: Mapped[date] = mapped_column(ForeignKey("base.purchase_date"))
    frame_serial: Mapped[str_20] = mapped_column(primary_key=True)
    frame_size_cm: Mapped[float_2]
    frame_material: Mapped[str_10]

    def __repr__(self):
        return self._set_repr()