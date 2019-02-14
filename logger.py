import logging

LOGGING_OPTS = {
    0: logging.ERROR,
    1: logging.WARNING,
    2: logging.INFO,
    3: logging.DEBUG
}


class Logger(object):
    # sets the logging level:
    #   0:  only errors will be logged
    #   1:  errors and warnings will be logged.
    #   3:  errors, warnings and info messages will be logged
    #   4:  debug messages will be logged too.
    logging_level = 3

    def __init__(self, loggername):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(LOGGING_OPTS.get(self.logging_level))
        fh = logging.FileHandler('TeleSpotify.log')
        formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s:\t %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)
