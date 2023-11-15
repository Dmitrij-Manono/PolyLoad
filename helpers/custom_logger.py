import logging
import inspect
import os


from coloredlogs import ColoredFormatter

# default log level values
# DEBUG: 10
# INFO: 20
# WARNING: 30
# ERROR: 40
# CRITICAL: 50
# EXCEPTION: 60



COLORED_FORMATTER="%(levelname)s %(asctime)s.%(msecs)d %(name)s %(shortened_path)s %(funcName)s %(lineno)d |%(process)d:%(thread)d| %(message)s"

DEFAULT_FORMATTER="%(levelname)s %(asctime)s.%(msecs)d %(name)s %(shortened_path)s %(funcName)s %(lineno)d |%(process)d:%(thread)d| %(message)s"

DATE_FORMAT='%Y-%m-%d %H:%M:%S'
COLORED_FIELD_STYLES={
    'lineno': {'color': 127},
    'name': {'color': 103},
    'levelname': {'color': 214, 'bold': True},
    'funcName': {'color': 103},
    'asctime': {'color': 103, 'bold': True},
    'message': {'color': 'white'},
    'filename': {'color': 103},
    'module': {'color': 103},
    'relativeCreated': {'color': 'green'},
    'msecs': {'color': 103, 'bold': True},
    'process': {'color': 103},
    'shortened_path': {'color': 103}
}

COLORED_LEVEL_STYLES={
    'info': {'color': 34, 'bold': False},
    'warning': {'color': 226, 'bold': True},
    'error': {'color': 196, 'bold': False},
    'debug': {'color': 27, 'bold': True},
    'critical': {'color': 'white', 'bold': True, 'background': 'red'},
    'exception': {'color': 196, 'bold': True},
    'alert': {'color': 166, 'bold': True},
    'user': {'color': 200, 'bold': True}
}


class CustomLogger(logging.Logger):
    def __init__(self, logger_name=__name__, log_path='logs/app.log', log_level=logging.DEBUG):
        super().__init__(logger_name, logging.DEBUG)  # Initialize the superclass with default log level

        # Custom Levels
        logging.addLevelName(10, "DEBUG")
        logging.addLevelName(15, "USER")
        logging.addLevelName(30, "INFO")
        logging.addLevelName(35, "ALERT")
        logging.addLevelName(40, "WARNING")
        logging.addLevelName(70, "ERROR")
        logging.addLevelName(80, "CRITICAL")
        logging.addLevelName(90, "EXCEPTION")
  

        # Console Handler for colored logging
        ch = logging.StreamHandler()
        colored_formatter = ColoredFormatter(fmt=COLORED_FORMATTER,
                                             datefmt=DATE_FORMAT,
                                             field_styles=COLORED_FIELD_STYLES,
                                             level_styles=COLORED_LEVEL_STYLES)
        ch.setFormatter(colored_formatter)
        self.addHandler(ch)

        # File Handler for file logging
        fh = logging.FileHandler(log_path)
        file_formatter = logging.Formatter(fmt=DEFAULT_FORMATTER, datefmt=DATE_FORMAT)
        fh.setFormatter(file_formatter)
        self.addHandler(fh)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        rv = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

        # Add a shortened path attribute
        path_parts = os.path.normpath(rv.pathname).split(os.sep)
        if len(path_parts) > 1:
            rv.shortened_path = os.path.join(path_parts[-2], path_parts[-1])
        else:
            rv.shortened_path = rv.pathname

        return rv

    def debug(self, message, *args, **kwargs):
        if self.isEnabledFor(10):
            self._log(10, message, args, **kwargs, stacklevel=2)

    def user(self, message, *args, **kwargs):
        if self.isEnabledFor(15):
            self._log(15, message, args, **kwargs, stacklevel=2)

    def info(self, message, *args, **kwargs):
        if self.isEnabledFor(30):
            self._log(30, message, args, **kwargs, stacklevel=2)
    
    def alert(self, message, *args, **kwargs):
        if self.isEnabledFor(35):
            self._log(35, message, args, **kwargs, stacklevel=2)
    
    def warning(self, message, *args, **kwargs):
        if self.isEnabledFor(40):
            self._log(40, message, args, **kwargs, stacklevel=2)

    def error(self, message, *args, **kwargs):
        if self.isEnabledFor(70):
            self._log(70, message, args, **kwargs, stacklevel=2)
    
    def critical(self, message, *args, **kwargs):
        if self.isEnabledFor(80):
            self._log(80, message, args, **kwargs, stacklevel=2)
    
    def exception(self, message, exc_info=True, *args, **kwargs):
        if self.isEnabledFor(90):
            self._log(90, message, args, **kwargs, stacklevel=2, exc_info=exc_info)

    
    



# test logger
if __name__ == "__main__":
    logger = CustomLogger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger.exception("exception message")
    logger.alert("alert message")
    logger.user("user message")

    try:
        x = 1/0
    except Exception as e:
        logger.exception(e)

    