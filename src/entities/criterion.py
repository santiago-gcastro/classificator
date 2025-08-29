import re
import os
import datetime

from abc import ABC, abstractmethod

from entities import file
from loggeable import loggeable

class DestinationCriterion(ABC, loggeable.IsLoggeable):
    def __init__(self):
        super()._init_logger(__name__)

    def calculate_destination(self, /, source_file, destination_path):
        if not isinstance(source_file, file.File):
            self._logger.error("Source file has to be a instance of File")
            return 
        return self._calculate(source_file, destination_path)

    @abstractmethod
    def _calculate(self, source_file, base_path):
        pass

class DateDestinationCriterion(DestinationCriterion):
    #\d{8}
    #\d{8}[_|-]\d{6}
    __patterns = {"\d{8}": "%Y%m%d"}
    def __init__(self):
        super().__init__()

    def _calculate(self, source_file, base_path):
        creationDate = self.__extractCreationDate(source_file)
        self._logger.debug(f"Creation time for {source_file.file_name()} is {creationDate}")
        year = creationDate.strftime("%Y")
        month = creationDate.strftime("%m")
        return os.path.join(base_path, year, month)
    
    def __extractCreationDate(self, source_file):
        name = source_file.file_name()
        parsed_time = None
        for pattern in list(self.__patterns):
            tokens = re.findall(pattern, name)
            for token in tokens:
                try:
                    parsed_time = datetime.datetime.strptime(token, self.__patterns[pattern])
                except TypeError|ValueError as error:
                    self._logger.error("{token} could not be parsed as Data due the error {error}")
        if parsed_time is None:
            return source_file.creation_time_stamp()
        return parsed_time

class TypeDestinationCriterion(DestinationCriterion):
    def _calculate(self, source_file, base_path):
        return os.path.join(base_path, source_file.file_type())
    
class OriginPathDestinationCriterion(DestinationCriterion):
    __path_chunk = None
    def __init__(self, command_criteria):
        super().__init__()
        if "=" in command_criteria:
            self.__path_chunk = command_criteria[command_criteria.rfind("=") + 1:]
        if self.__path_chunk is None:
            self._logger.warning("Criteria path has to include a value as path=value")

    def _calculate(self, source_file, base_path):
        if self.__path_chunk is not None:
            out_path = base_path
            path_uncollapse = os.path.split(source_file.file_path())
            for folder in path_uncollapse:
                if self.__path_chunk in folder:
                    out_path = os.path.join(out_path, folder)
            return out_path
        return base_path


class CriterionFactory:
    @staticmethod
    def get_criteria(criteria_command):
        destinationCriteria = []
        criteria = criteria_command.split(",")
        for criterion in criteria:
            if criterion == "date" :
                destinationCriteria.append(DateDestinationCriterion())
            elif criterion == "type" :
                destinationCriteria.append(TypeDestinationCriterion())
            elif "path" in criterion:
                destinationCriteria.append(OriginPathDestinationCriterion(criterion))
            else:
                loggeable.IsLoggeable.get_logger(CriterionFactory.__name__, __name__).warning(f"Criteria #{criterion}# not valid. Only date or type are valid criteria")
        return destinationCriteria
