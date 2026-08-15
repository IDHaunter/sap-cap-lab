import logging
import os
import sys
import re
from datetime import datetime
from typing import Optional

DEFAULT_LOG_LEVEL = logging.DEBUG

class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO, is_stderr=False):
        self.logger = logger
        self.log_level = log_level
        self.is_stderr = is_stderr
        self.linebuf = ''

    def write(self, buf):
        # Remove ANSI control characters (e.g. \x1b[A\x1b[A)
        buf_cleaned = re.sub(r'\x1b\[[0-9;]*[mK]', '', buf).strip()
        buf_cleaned = "\n".join(filter(bool, buf_cleaned.splitlines()))

        if not buf_cleaned:
            return  # Skipping empty lines

        # Log stderr as ERROR only if the message looks like an error
        if self.is_stderr:
            level = logging.ERROR if re.search(r'\b(error|exception)\b', buf_cleaned, re.IGNORECASE) else self.log_level
        else:
            level = self.log_level

        for line in buf_cleaned.splitlines():
            self.logger.log(level, line.rstrip())

    def flush(self):
        # Method required to conform to file-like API (e.g., sys.stdout), but no flushing needed
        pass


class DateRotatingFileHandler(logging.FileHandler):
    def __init__(self, log_dir, module_name, log_level=logging.DEBUG):
        self.log_dir = log_dir
        self.module_name = module_name
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        log_filename = f'{self.module_name}_{self.current_date}.log'
        log_filepath = os.path.join(self.log_dir, log_filename)
        super().__init__(log_filepath, encoding='utf-8')
        self.setLevel(log_level)
        # This formatter is responsible for logs that are written to files.
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))

    def emit(self, record):
        new_date = datetime.now().strftime('%Y-%m-%d')
        if new_date != self.current_date:
            self.current_date = new_date
            log_filename = f'{self.module_name}_{self.current_date}.log'
            log_filepath = os.path.join(self.log_dir, log_filename)
            self.stream.close()
            self.baseFilename = log_filepath
            self.stream = self._open()
        super().emit(record)

class LoggerNameAliasFilter(logging.Filter):
    """Rewrites specific logger names for cleaner log output (display only)."""
    ALIASES = {
        'uvicorn.error': 'uvicorn',
        'uvicorn.access': 'uvicorn',
    }

    def filter(self, record):
        record.name = self.ALIASES.get(record.name, record.name)
        return True

class ModuleLogger:
    def __init__( self, module_name: str, log_dir: str = 'logs', log_level: Optional[int] = None ):
        self.module_name = module_name
        self.log_dir = log_dir
        if not log_level:
            self.log_level = ModuleLogger.get_logger_level_from_env(module_name)
        else:
            self.log_level = log_level
        self.log_level_name = ModuleLogger.get_logger_level_name (self.log_level)
        self.logger = logging.getLogger(self.module_name)
        self._setup_logger()

    @staticmethod
    def get_logger_level_from_env(module_name: str) -> int:
        log_level_env = os.getenv(f"{module_name.strip().upper()}_LOG_LEVEL", "").strip().upper()
        if not log_level_env:
            print(f"WARNING - [ModuleLogger] - LOG LEVEL from env variable is empty")

        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'INF': logging.INFO,
            'WARNING': logging.WARNING,
            'WARN': logging.WARNING,
            'ERROR': logging.ERROR,
            'ERR': logging.ERROR,
            'CRITICAL': logging.CRITICAL,
            'CRIT': logging.CRITICAL,
        }

        return levels.get(log_level_env, DEFAULT_LOG_LEVEL)

    @staticmethod
    def get_logger_level_name(level: int) -> str:
        reverse_levels = {
            logging.DEBUG: 'DEBUG',
            logging.INFO: 'INFO',
            logging.WARNING: 'WARNING',
            logging.ERROR: 'ERROR',
            logging.CRITICAL: 'CRITICAL',
        }
        return reverse_levels.get(level, 'UNKNOWN')

    def _setup_logger(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Set up the root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)

        if not root_logger.hasHandlers():
            # File handler with date rotation
            file_handler = DateRotatingFileHandler(self.log_dir, self.module_name, self.log_level)
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)

            # Formatter (This formatter is responsible for the logs that are written to console)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
            console_handler.setFormatter(formatter)

            # Filter to rewrite logger names for cleaner output
            name_filter = LoggerNameAliasFilter()
            file_handler.addFilter(name_filter)
            console_handler.addFilter(name_filter)

            # Adding handlers to root logger
            root_logger.addHandler(file_handler)
            root_logger.addHandler(console_handler)

        # Redirect stdout to INFO, stderr — filter errors
        try:
            sys.stdout = StreamToLogger(root_logger, logging.INFO, is_stderr=False)
            sys.stderr = StreamToLogger(root_logger, logging.INFO, is_stderr=True)
        except Exception as e:
            print(f"ERROR - [ModuleLogger] - Failed to redirect stdout/stderr: {e}")

    def get_logger(self):
        return self.logger


"""
Initialization example for settings or main module:

    from app.utils.module_logger import ModuleLogger, get_logger_level
    module_logger = ModuleLogger(module_name='APP_NAME', log_dir='LOGS_DIR')
    logger = module_logger.get_logger()

    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')

Initialization example for settings or main module:

Since ModuleLogger already configures the root logger (root_logger),
there is no need to import logger from settings (or main).
All modules will automatically pick up the configuration.

    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
"""
