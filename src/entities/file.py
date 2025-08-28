import os
import datetime
import logging

logger = logging.getLogger(__name__)

class File:
    def __init__(self, /,name, path):
        self.__name = name
        self.__path = path
        self.__creation_time = os.path.getctime(self.full_path())
        print(f"Name: {self.__name} path - {self.__path}")

    def full_path(self):
        return os.path.join(self.__path, self.__name)

    def file_name(self):
        return self.__name
    
    def file_type(self):
        return self.__name[self.__name.rfind(".") + 1:]

    def creation_time_stamp_as_string(self):
        return datetime.datetime.fromtimestamp(self.__creation_time).strftime("%Y-%m-%d %H:%M:%S")

    def creation_time_stamp(self):
        return  datetime.datetime.fromtimestamp(self.__creation_time)
