import shutil
import os
import re

class FileManager:
    def copy(self, /,origin, destination):
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        if os.path.isfile(destination):
            self.copy(origin, self.__new_destiny(destination))
            
        try:
            shutil.copy(origin, destination)
        except shutil.SameFileError as sameFileError:
            print(sameFileError)

    def __new_destiny(self, destiny):
        token_pattern = "[(]\\d+[)]"
        path_name = destiny[:destiny.rfind(".")]
        sufix = destiny[destiny.rfind("."):]
        tokens = re.findall(token_pattern, path_name)
        duplicated_mark = tokens.pop() if len(tokens) > 0 else None
        if not self.__has_duplicated_mark(path_name, duplicated_mark):
            return f"{path_name} (1){sufix}"
        
        next = self.__calculate_next(duplicated_mark)
        return f"{self.__replace_last_occurrence(path_name, duplicated_mark, next)}{sufix}";

    def __has_duplicated_mark(self, name, duplicated_mark):
        return duplicated_mark is not None and name.endswith(duplicated_mark)

    def __replace_last_occurrence(self, text, pattern, replacement):
        index = text.rfind(pattern)
        if index == -1:
            return text
        
        return text[:index] + replacement + text[index + len(pattern):]
    
    def __calculate_next(self, duplicated_mark):
        return f"({int(duplicated_mark[1:-1]) + 1})"
        