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

class Stem(ComponentBase):
    __tablename__ = "stem"

    quill_style: Mapped[str_20]

    height_mm: Mapped[float_2]
    reach_mm: Mapped[float_2]
    quill_diameter_mm: Mapped[float_2]
    steerer_diameter_mm: Mapped[float_2]
    clamp_diameter: Mapped[float_2]