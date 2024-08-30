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

class BottomBracket(ComponentBase):
    __tablename__ = 'bottom_bracket'

    threading: Mapped[str_10]
    bearing_type: Mapped[str_20]
    spindle_material: Mapped[str_20]
    spindle_length_mm: Mapped[float_2]
    crank_mount_type: Mapped[str_20]

    frame: Mapped['Frame'] = relationship(back_populates='bottom_bracket')