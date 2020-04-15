import sys
import datetime
import logging
import subprocess
from logging import handlers

import watchtower

LOG_LEVELS = {
    'mute': logging.CRITICAL + 10,
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}

DEFAULT_LOG_MAX_SIZE = 104857600  # 100 MB
DEFAULT_LOG_MAX_FILES = 100


def get_short_git_version(path='.'):
    data = subprocess.check_output(['git', '-C', path, 'log', '--pretty=%h-%at', '-1']).strip().decode("utf-8")
    shorthash, ts = data.split('-')
    date = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d-%H%M')
    return '%s-%s' % (shorthash, date)


def get_git_branch(path='.'):
    try:
        return subprocess.check_output(['git', '-C', path, 'symbolic-ref', '--short', 'HEAD']).strip().decode("utf-8")
    except subprocess.CalledProcessError:
        return 'DETACHED'


def get_logger(app_name,
               logfile=None,
               log_format='%(asctime)s: %(levelname)-8s %(message)s',
               file_level=logging.DEBUG,
               console_level=logging.INFO,
               num_backup_files=DEFAULT_LOG_MAX_FILES,
               log_file_size=DEFAULT_LOG_MAX_SIZE):  # 100 MB
    """Get the logger, set parameters on first use only (see set_logger_params for details)."""

    logger = logging.getLogger(app_name)
    if not logger.handlers:  # only set params on first use
        set_logger_params(app_name, logfile, log_format,
                          file_level, console_level,
                          num_backup_files, log_file_size)
    return logger


def set_logger_params(app_name,
                      logfile=None, log_format=None, file_level=None, console_level=None,
                      num_backup_files=DEFAULT_LOG_MAX_FILES, log_file_size=DEFAULT_LOG_MAX_SIZE):
    """Override/reset logger parameters (keep what you don't want to change as None).
    You need to reset the file name if you want to change the backup files or max. size.
    Set logfile='CLOUDWATCH' to use CloudWatch instead of a local file for logging."""

    logger = logging.getLogger(app_name)

    if isinstance(file_level, str):
        file_level = LOG_LEVELS[file_level]
    if isinstance(console_level, str):
        console_level = LOG_LEVELS[console_level]

    if not logger.handlers:
        if logfile == 'CLOUDWATCH':
            # XXX this will crash if you don't have your AWS credentials stored in ~/.aws
            # TODO add the option of setting AWS credentials somehow?
            file_handler = watchtower.CloudWatchLogHandler()
        elif logfile is not None:
            file_handler = handlers.RotatingFileHandler(
                logfile, 'a', log_file_size, num_backup_files, 'UTF-8')
        else:
            file_handler = logging.NullHandler()
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(console_handler)
    else:
        file_handler, console_handler = logger.handlers
        # changed settings of file logging: need to recreate the file
        if logfile is not None:
            logger.removeHandler(file_handler)
            logger.removeHandler(console_handler)
            if logfile == 'CLOUDWATCH':
                file_handler = watchtower.CloudWatchLogHandler()
            else:
                file_handler = handlers.RotatingFileHandler(
                    logfile, 'a', log_file_size, num_backup_files, 'UTF-8')
            file_handler.setFormatter(console_handler.formatter)
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

    # set levels & formatting
    logger.setLevel(logging.DEBUG)  # this is the lowest level that is considered by any handler
    if log_format is not None:
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
    if file_level is not None:
        file_handler.setLevel(file_level)
    if console_level is not None:
        console_handler.setLevel(console_level)
