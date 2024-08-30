from ._table_bases import Base
from .frame import Frame

from sqlalchemy import ForeignKey
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
    
