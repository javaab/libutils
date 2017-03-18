import unittest
import sys

from libutils.log_formatters import ColoredFormatter, LevelFormatter


class TestLogUtils(unittest.TestCase):

    def setUp(self):
        pass

    def _formatter_isnt_broken(self, formatter):
        try:
            import logging
            logger = logging.getLogger()
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(formatter)
            logger.debug('DEBUG message')
            logger.info('INFO message')
            logger.warn('WARN message')
            logger.error('ERROR message')
            logger.critical('CRITICAL message')
        except Exception as e:
            self.fail("Logging is broken: %s" % e)

    def test_log_color_formatter_isnt_broken(self):
        self._formatter_isnt_broken(ColoredFormatter())

    def test_log_level_formatter_isnt_broken(self):
        self._formatter_isnt_broken(LevelFormatter())
