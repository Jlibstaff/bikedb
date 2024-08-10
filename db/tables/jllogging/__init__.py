import os

from io import StringIO
from logging import StreamHandler, FileHandler, Logger, Formatter
from logging import DEBUG, INFO, ERROR, WARNING
from typing import Union

# Consider adding a helper function to log the contents of dicts using a single
# function call. This could clean up a lot of for loops and multi-line variable 
# debugging.

class JLLogger(Logger):
    """Custom Logger class to handle formatting and output in a consistent way"""
    def __init__(self, name: str):
        super().__init__(name)
        self.setLevel(DEBUG)
        self.cwd = os.getcwd()
        
    def _format_setup(self, format_type: Union[str, None] = None) -> Formatter:
        self.standard_formatter = Formatter('%(asctime)s %(name)s:%(funcName)s:%(lineno)s   -   %(message)s')
        self.string_formatter = Formatter('%(asctime)s %(name)s:%(funcName)s:%(lineno)s   -   %(message)s')
        if format_type == 'string':
            return self.string_formatter
        return self.standard_formatter
    
    def terminal_setup(self, log_level: int) -> None:
        self.terminal_handler = StreamHandler()
        self.terminal_handler.setLevel(log_level)
        self.terminal_handler.setFormatter(self._format_setup('string'))
        self.addHandler(self.terminal_handler)
        
    def stream_setup(self, log_level: int) -> None:
        self.stream = StringIO()        
        self.string_handler = StreamHandler(self.stream)
        self.string_handler.setLevel(log_level)
        self.string_handler.setFormatter(self._format_setup('string'))
        self.addHandler(self.string_handler)
        
    def file_setup(self, filename: str, log_level: int) -> None:
        file_handler = FileHandler(
            filename=filename,
            mode='a',
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(self._format_setup())
        self.addHandler(file_handler)

    def log_dict(self, **kwargs) -> None:
        complex_types = [list, dict, tuple, set]

        for k, v in kwargs.items():
            if type(v) not in complex_types:
                self.debug(f'\t{k}: {v}')
            elif not isinstance(v, dict):
                self.debug(f'\t{k}:')
                for item in v:
                    self.debug(f'\t\t{item}')
            else:
                self.debug(f'\t{k}:')
                for kk, vv in v.items():
                    self.debug(f'\t\t{kk}: {vv}')

        # This should be fleshed out to be recursive for multi-level
        # nested dicts, but this will work for now. 


    def get_log_stream(self) -> dict:
        log_stream_dict = {
            self.name: self.stream
        }
        
        return log_stream_dict