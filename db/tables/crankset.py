from ._table_bases import ComponentBase
#from .frame import Frame

from sqlalchemy.orm import Mapped
#from sqlalchemy.orm import relationship

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

class Crankset(ComponentBase):
    __tablename__ = 'crankset'
    
    arm_length_mm: Mapped[float_2]
    bb_type: Mapped[str_20]
    spindle_type: Mapped[str_20]
    chainring_bolt_qty: Mapped[int]
    bolt_circle_diameter: Mapped[float_2]
    chainring_qty: Mapped[int]
    pedal_thread: Mapped[str_10]