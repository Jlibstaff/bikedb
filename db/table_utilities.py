#!/media/jll/Occam/dev/repos/personal/bikedb/.venv/bin/python

from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from typing import Union, List

import os
import pandas as pd
import shutil
import tables
from tables import Base

def get_table_columns() -> dict: 
    table_dict = {}

    for _class in tables.__all__:
        class_path = str(_class).split('\'')[1]
        dot_last = class_path.rindex('.')
        class_name = class_path[dot_last+1:]
        table_class = get_table_class(class_name)
        table_dict.update(table_class)
    return table_dict

def get_table_class(table_name: str) -> dict:
    # print(f'{type(table_name)}: {table_name}')
    table_class = getattr(import_module('tables'), table_name)
    class_instance = table_class()
    print(type(class_instance))
    table_columns = class_instance._get_column_names()
    class_dict = {table_name: table_columns}
    # print(f'    class_dict: {class_dict}')
    return class_dict

def get_session(engine: Engine) -> Session:
    
    Session = sessionmaker(engine)

    with Session.begin() as session:
        return session

def build_tables(engine: Engine) -> None:
    Base.metadata.create_all(engine)
    
def export_templates():
    table_dict = get_table_columns()
    base_path = '/'.join(os.getcwd().split('/')[:-1])
    template_path = os.path.join(base_path, 'templates')
    if not os.path.isdir(template_path):
        os.makedirs(template_path)
    for k, v in table_dict.items():
        columns = {item: [] for item in v}
        df = pd.DataFrame(columns)
        df.to_csv(f'{template_path}/{k}_template.csv', sep='|', index=False)

def input_setup() -> None:
    base_path = '/'.join(os.getcwd().split('/')[:-1])
    template_path = os.path.join(base_path, 'templates')
    input_path = os.path.join(base_path, 'input')
    
    if not os.path.isdir(template_path):
        export_templates()
    if not os.path.isdir(input_path):
        os.makedirs(input_path)
    for f in os.listdir(template_path):
        template_file = os.path.join(template_path, f)
        input_file = os.path.join(input_path, f.replace('_template', ''))
        shutil.copy(template_file, input_file)


if __name__ == '__main__':
    engine = create_engine(
        'postgresql+psycopg2://postgres:23Kuelap!@172.18.0.3:5432/bikedb'
    )
    template_path = os.path.join('..','templates')
    # build_tables(engine)
