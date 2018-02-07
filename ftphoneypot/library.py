# Murat B. on github..

import string
import random
import logging
import datetime
from logging import handlers
from configobj import ConfigObj

LOG_FILE = "/opt/ftphoneypot/logs/ftphoneypot.log"
CONF_FILE = "/opt/ftphoneypot/config.cfg"


def id_generate(size, chars=string.ascii_uppercase + string.digits):
    """
    Queue id generator
    :param size: Size Integer
    :param chars: Char Detail
    :return:
    """
    return ''.join(random.choice(chars) for _ in range(size))


class LogOperation(object):
    """
    Logger Class
    """
    __LOGGER = None

    def __init__(self):
        """
        First initialization
        :param url: Git Remote URL
        :param branch: Branch
        :param log_file: Log File defination
        """
        global LOG_FILE
        self.__LOGGER = logging.getLogger(__name__)
        self.__LOGGER.setLevel(logging.INFO)
        HANDLER = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=20 * 1024 * 1024, backupCount=5)
        HANDLER.setLevel(logging.INFO)
        FORMATTER = logging.Formatter(
            '%(asctime)s.%(msecs)03d [%(process)s] %(levelname)s: - '
            '%(message)s', "%d/%m/%Y %H:%M:%S")
        HANDLER.setFormatter(FORMATTER)
        if self.__LOGGER.hasHandlers():
            self.__LOGGER.handlers.clear()
        self.__LOGGER.addHandler(HANDLER)

    def log_warning(self, message):
        """
        Warning logger
        :param message: Warning log message
        :return: None
        """
        self.__LOGGER.warn(message)

    def log_error(self, message):
        """
        Error logger
        :param message: Error log message
        :return: None
        """
        self.__LOGGER.error("Error : " + str(message))

    def log_info(self, message):
        """
        Normal logger
        :param message: Log message
        :return: None
        """
        self.__LOGGER.info(message)


class ConfigParse(object):
    """
    Config Parser Class
    """

    def __init__(self, log_object):
        """
        First initialization
        :param dir: Git directory
        :param url: Git remote url
        :param branch: branch
        :param log_object: created log object
        """
        global CONF_FILE, LOG_FILE
        self.__config_db = ConfigObj(CONF_FILE)
        self.__log_object = log_object
        self.__return_map = dict()
        for key, value in self.__config_db.iteritems():
            self.__return_map.update({key: value})

    def get_item(self, q_key):
        """
        Return map dict from loaded config parse object
        :return: Dictionary
        """
        if q_key in self.__return_map.keys():
            return dict(self.__return_map.get(q_key))
        else:
            return dict()


class HeaderWriter(object):
    """
    Header write operation
    """

    def __init__(self, log_object):
        """
        First initialization
        :param log_object: created log object
        """
        self.__log_object = log_object

    def write_header(self, ip, qid):
        """
        Write header data to file
        :param ip: ip string
        :param qid: queue id string
        :return: None
        """
        time = datetime.datetime.now().strftime('%s')
        filename = "/opt/ftphoneypot/headers/" + time + "-" + qid
        data = "ftp;" + time + ";" + ip + ";" + qid
        try:
            with open(filename, 'w') as out:
                out.write(data + '\n')
        except Exception as ex:
            self.__log_object.log_warning("Not write the header : " + str(ex))


class SMTPCommandWriter(object):
    """
    SMTP command writer
    """

    def __init__(self, log_object):
        """
        First initialization
        :param log_object: created log object
        """
        self.__log_object = log_object

    def write_commands(self, data, qid):
        """
        Write commands data to file
        :param data_list:
        :return: None
        """
        filename = "/opt/ftphoneypot/commands/" + qid
        try:
            with open(filename, 'a') as out:
                out.write(data + '\n')
        except Exception as ex:
            self.__log_object.log_warning("Not write the command : " + str(ex))


class DATAWriter(object):
    """
    Data Write
    """

    def __init__(self, log_object):
        """
        First initialization
        :param log_object: created log object
        """
        self.__log_object = log_object

    def write_data(self, data, filename):
        filename = "/opt/ftphoneypot/mails/" + filename
        try:
            with open(filename, 'a') as out:
                out.write(data + "\n")
        except Exception as ex:
            self.__log_object.log_warning("Not write the data : " + str(ex))
