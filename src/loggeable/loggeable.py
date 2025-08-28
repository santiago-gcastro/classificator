import logging

class IsLoggeable:
    @staticmethod
    def get_logger(caller, source):
        return logging.getLogger(source)

    def _init_logger(self, source):
        self._logger = logging.getLogger(source)
    