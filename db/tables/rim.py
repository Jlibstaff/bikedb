from ._table_bases import ComponentBase
from .frame import Frame

from sqlalchemy.orm import Mapped
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

    frame: Mapped['Frame'] = relationship(back_populates='rim')