import logging
import os

from exceptions import ConfigurationError

LOG_LEVEL = 'AWSTOOLS_LOG_LEVEL'
LOG_VERBOSITY = 'AWSTOOLS_LOG_VERBOSITY'
LOG_VERBOSE = 'VERBOSE'
LOG_CONCISE = 'CONCISE'


def get_log_format():
    """
    Return the log format to use
    """
    try:
        log_format_verbosity = os.environ[LOG_VERBOSITY].upper().strip()
    except KeyError:
        log_format_verbosity = LOG_VERBOSE

    if log_format_verbosity == LOG_CONCISE:
        format = '%(asctime)s %(name)s (%(lineno)d) %(levelname)s: %(message)s'
    else:           # verbose by default
        format = '%(asctime)s %(pathname)s %(name)s (%(lineno)d) '\
                 '%(levelname)s: %(message)s'

    return format


def get_logger(name):
    """
    Set up a logger. The log level can be set by setting an environment
    variable called AWSTOOLS_LOG_LEVEL to a valid log level, or NONE to disable
    all logging output.

    string name: The name of the logger. Set this to __name__ in the calling
    code (unless you have a VERY good reason
    not to)

    returns: A Logger instance
    """
    log = logging.getLogger(name)

    if not log.handlers:
        logging.basicConfig(format=get_log_format())

    try:
        log_level = getattr(logging, os.environ[LOG_LEVEL].upper())
    except AttributeError:
        log_level = os.environ[LOG_LEVEL].upper()
        if log_level != 'NONE':
            raise ConfigurationError("'%s' is not a valid log level. Use a "
                                     "valid log level or 'NONE' to disable "
                                     "logging output." % log_level)
    except KeyError:
        log_level = logging.INFO

    if log_level == 'NONE':
        log.disabled = True
    else:
        log.setLevel(log_level)

    log.debug("Logger configured for %s" % name)

    return log
