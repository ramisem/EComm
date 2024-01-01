import logging


class Logger:
    __logger = None
    __logger_error = None

    def __init__(self):
        self.__logger = logging.getLogger('django')
        self.__logger_error = logging.getLogger('error_log')

    def info(self, message):
        self.__logger.info(message)

    def error(self, error_message):
        self.__logger_error.error(error_message, exc_info=True)


print_log = Logger()
