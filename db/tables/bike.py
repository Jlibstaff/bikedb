#!/media/jll/Occam/dev/sandbox/bikedb/.venv/bin/python3

from datetime import date
from hashlib import sha1

from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy import JSON, ARRAY
from sqlalchemy import ExecutionContext
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from typing import (
    Any, 
    Annotated,
    List
    )

# type annotations, not necessary, but nice to have:
float_2 = Annotated[float, 2]
str_40 = Annotated[str, 40]
str_20 = Annotated[str, 20]
str_10 = Annotated[str, 10]
year = Annotated[int, 4]

def _hash_id(context: ExecutionContext) -> str:
    """Generate a hash string from the values of the columns named in `hash_keys`

    Parameters:
        context: the context of the sqlalchemy table object
        
    Returns: 
        id: the hash string generated to be the primary key value
    """
    hash_keys = [
        'production_year', 
        'manufacturer', 
        'model_name', 
        'purchase_date'
    ]
    hashstring = ''
    for key in hash_keys:
        hash_string += f'_{context.get_current_parameters()[key]}'
        id = sha1(hash_string.encode()).hexdigest()
        return id

class AnnotationBase(DeclarativeBase):
    """Class to create type annotations for all table objects"""
    
    type_annotation_map = {
        str_40: String(40),
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
    """Class to set up default columns and functions for all table objects"""
    def __init__(self):
        super().__init__()
    
    __abstract__ = True
    
    id: Mapped[str_40] = mapped_column(primary_key=True, default=_hash_id)
    production_year: Mapped[year]
    manufacturer: Mapped[str_20]
    model_name: Mapped[str_20]
    stamped_codes: Mapped[dict[str, Any]]
    style: Mapped[str_20]
    features: Mapped[dict[str, Any]]

    material: Mapped[dict[str, Any]]
    weight_spec_g: Mapped[float_2]
    weight_actual_g: Mapped[float_2]

    purchase_date: Mapped[date]
    purchase_price: Mapped[float_2]
    value_low_usd: Mapped[float_2]
    value_avg_usd: Mapped[float_2]
    value_high_usd: Mapped[float_2]
    
    # create snapshot of local variables (column objects)
    _locals = locals()

    def _get_annotations(self) -> dict:
        """Get annotations for both parent and child objects
        
        Returns:
            _annotations: dictionary of column names for the table object
        """
        _annotations = self.__annotations__
        _annotations.update(self._locals['__annotations__'])

        # check to see if it's more efficient to call this once from the 
        # class-scope and use the variable multiple times, or if it's 
        # better to call this on-demand.
        # presumably, on-demand makes the most sense, unless both of the
        # functions that use this are used frequently.
        return _annotations

    def __repr__(self) -> str:
        """Set __repr__ output to include all columns of a derived class.
        
        Returns: 
            repr: string representation of object in __repr__ format
        """
        _annotations = self._get_annotations()
        repr_head = f"<{self.__class__.__name__}("
        repr_body_list = [f'{k}={v}' for k, v in _annotations.items()]
        repr_body = ','.join(repr_body_list)
        repr_tail = ')>'
        repr = ''.join([repr_head, repr_body, repr_tail])
        return repr
    
    def _get_relationship_name(self) -> str:
        return (str(self.__class__.__mro__)
            .split('.')[1]
            .split('\'')[0]
            .lower()
        )
    
    def get_columns(self) -> None:
        """Print the column names of the current table object"""
        _annotations = self._get_annotations()
        print(f'{self.__class__.__name__}:')
        for k, v in _annotations.items():
            print(f'    {k}: {v}')
    
class ComponentBase(Base):
    """Class to set up standard columns for component table objects"""
    def __init__(self):
        super().__init__()
    
    __abstract__ = True
    
    frame_serial: Mapped[str_20] = mapped_column(ForeignKey('frame.serial'))
    manufacturer: Mapped[str_20] = mapped_column(primary_key=True)
    component_group: Mapped[str_20] = mapped_column(primary_key=True)
    model_name: Mapped[list[str]] = mapped_column(primary_key=True)
    stamped_codes: Mapped[dict[str, Any]] = mapped_column(primary_key=True)

    @declared_attr
    def frame(self) -> Mapped['Frame']:
        return relationship(back_populates=self._get_relationship_name(self))
    
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
class Fork(Base):
    __tablename__ = "fork"

    manufacturer: Mapped[str_20] = mapped_column(primary_key=True)
    stamped_codes: Mapped[dict[str, Any]] = mapped_column(primary_key=True)
    frame_serial: Mapped[str_20] = mapped_column(ForeignKey('frame.serial'))
   
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

    frame: Mapped['Frame'] = relationship(back_populates='fork')
    
class SeatPost(ComponentBase):
    __tablename__ = "seatpost"
    
    length_mm: Mapped[float_2]
    diameter_mm: Mapped[float_2]
    clamp_type: Mapped[str_20]

class Saddle(ComponentBase):
    __tablename__ = "saddle"
   
    dimensions_lwh_cm: Mapped[list[int]]

class Stem(ComponentBase):
    __tablename__ = "stem"

    quill_style: Mapped[str_20]

    height_mm: Mapped[float_2]
    reach_mm: Mapped[float_2]
    quill_diameter_mm: Mapped[float_2]
    steerer_diameter_mm: Mapped[float_2]
    clamp_diameter: Mapped[float_2]
"""
class HandleBars(ComponentBase):
    __tablename__ = 'handlebars'
    dimensions: Mapped[dict[str, Any]]
    clamping_diameter: Mapped[float_2]
    bar_diameter: Mapped[float_2]

class BrakeLevers(ComponentBase):
    __tablename__ = 'brake_levers'
    
    bar_type: Mapped[str_20]
    clamp_size: Mapped[float_2]
    lever_color: Mapped[str_10]
    hood_color: Mapped[str_10]

class Brakes(ComponentBase):
    __tablename__ = 'brakes'
    
    actuation_type: Mapped[str_20]
    position: Mapped[str_10]
    
class Shifters(ComponentBase):
    __tablename__ = 'shifters'
    
    indexed: Mapped[bool]
    capacity: Mapped[int]
    mount_type: Mapped[str_20]

class DerailleurFront(ComponentBase):
    __tablename__ = 'front_derailleur'
    
    capacity: Mapped[int]
    mount_type: Mapped[str_20]

class DerailleurRear(ComponentBase):
    __tablename__ = 'rear_derailleur'
    
    capacity: Mapped[int]
    mount_type: Mapped[str_20]
    
    cage_type: Mapped[str_10]
    sprocket_diameter_mm: Mapped[float_2]
    sprocket_tooth_qty: Mapped[int]
    sprocket_bearing_type: Mapped[str_20]

class Crankset(ComponentBase):
    __tablename__ = 'crankset'
    
    arm_length_mm: Mapped[float_2]
    bb_type: Mapped[str_20]
    spindle_type: Mapped[str_20]
    chainring_bolt_qty: Mapped[int]
    bolt_circle_diameter: Mapped[float_2]
    chainring_qty: Mapped[int]
    pedal_thread: Mapped[str_10]

class Pedal(ComponentBase):
    __tablename__ = 'pedal'

    toe_clips: Mapped[bool]
    clip_cleat_type: Mapped[str_20]

class FreewheelCasette(ComponentBase):
    __tablename__ = 'freewheel_cassette'

    gear_qty: Mapped[int]
    low_teeth: Mapped[int]
    high_teeth: Mapped[int]

class BottomBracket(ComponentBase):
    __tablename__ = 'bottom_bracket'

    threading: Mapped[str_10]
    bearing_type: Mapped[str_20]
    spindle_material: Mapped[str_20]
    spindle_length_mm: Mapped[float_2]
    crank_mount_type: Mapped[str_20]

class Hub(ComponentBase):
    __tablename__ = 'hub'

    spacing_mm: Mapped[float_2]
    axle_type: Mapped[str_20]
    bearing_type: Mapped[str_20]
    spoke_qty: Mapped[int]
    flange_diameter_mm: Mapped[float_2]
    hub_position: Mapped[str_10]
    
class Rim(ComponentBase):
    __tablename__ = 'rim'

    nominal_size: Mapped[str_20]
    internal_diameter_mm: Mapped[float_2]
    external_diameter_mm: Mapped[float_2]
    tire_mount_type: Mapped[str_20]
    spoke_qty: Mapped[int]
    valve_type: Mapped[str_10]
    internal_width_mm: Mapped[float_2]
    external_width_mm: Mapped[float_2]

class OtherComponent(ComponentBase):
    __tablename__ = 'other_component'
"""