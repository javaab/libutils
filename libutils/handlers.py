import re

from logging.handlers import (
	SocketHandler,
	DatagramHandler,
	BaseRotatingHandler,
)

import os.path
import time
from datetime import datetime


class TCPLogstashHandler(SocketHandler):
	"""
		A SocketHandler that does not pickle records
	"""
	def emit(self, record):
		try:
			s = self.format(record) + b'\n'
			self.send(s)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)

class UDPLogstashHandler(DatagramHandler):
	"""
		A DatagramHandler that does not pickle records
	"""
	def emit(self, record):
		try:
			s = self.format(record) + b'\n'
			self.send(s)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			self.handleError(record)

class GenRotatingFileHandler(BaseRotatingHandler):
	"""
	From lib/geneity/lib/LoggingHandlers

	Handler for logging to a file, rotating the log file at certain timed
	intervals.
	"""

	def __init__(self, base_filename, suffix_filename='', when='H',
				encoding=None, log_name_format=None, log_time_format={}):

		#
		# Control log file name
		#
		if log_time_format == {}:
			self.log_time_format = {
				"S": "%Y%m%d_%H%M%S",
				"M": "%Y%m%d_%H%M",
				"H": "%Y%m%d_%H",
				"D": "%Y%m%d"
			}
		else:
			self.log_time_format = log_time_format
		self.log_time_format.update(log_time_format)

		if log_name_format == None:
			self.log_name_format = "%(name)s.%(time)s.%(suffix)s"
		else:
			self.log_name_format = log_name_format

		self.when = when.upper()

		ts = time.time()
		currentTime = int(ts)
		offset = datetime.fromtimestamp(ts) - datetime.utcfromtimestamp(ts)
		self.offset_secs = offset.seconds

		if self.when.startswith('S'):
			self.interval = 1
		elif self.when.startswith('M'):
			self.interval = 60
		elif self.when.startswith('H'):
			self.interval = 60 * 60
		elif self.when.startswith('D'):
			self.interval = 60 * 60 * 24
		else:
			raise ValueError("Invalid rollover interval specified: %s" % self.when)

		lastRoll = currentTime - (currentTime % self.interval)
		self.rolloverAt = lastRoll + self.interval - self.offset_secs

		tt = time.localtime(lastRoll)

		filename = self.get_filename(base_filename, tt, suffix_filename)

		BaseRotatingHandler.__init__(self, filename, 'a', encoding)
		self.baseFilename = os.path.abspath(base_filename)
		self.suffix_filename = suffix_filename


	def shouldRollover(self, record):
		"""
		Determine if rollover should occur

		record is not used, as we are just comparing times, but it is needed so
		the method siguratures are the same
		"""
		if int(time.time()) >= self.rolloverAt:
			return 1

		return 0

	def get_filename(self, base_filename, tt, suffix):
		log_params = {
			'time': time.strftime(self.log_time_format[self.when[0]], tt),
			'name': os.path.basename(base_filename),
			'suffix': suffix
		}

		dirname = os.path.dirname(base_filename)

		if not os.path.exists(dirname):
			os.mkdir(dirname)

		filename = os.path.join(
			dirname,
			self.log_name_format % log_params
		)

		return filename

	def doRollover(self):
		self.stream.close()

		t = int(time.time())

		while t >= self.rolloverAt:
			self.rolloverAt += self.interval

		tt = time.localtime(self.rolloverAt - self.interval)

		filename = self.get_filename(
			self.baseFilename, tt, self.suffix_filename)

		self.stream = open(filename, 'a')

