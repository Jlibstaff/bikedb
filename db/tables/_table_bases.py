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
    Callable,
    List
    )

# type annotations, not necessary, but nice to have:
float_2 =  Annotated[float, 2]
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
    #type_annotations
    

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
    
