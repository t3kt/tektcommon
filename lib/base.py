print('common/base.py initializing')

try:
	import common_util as util
except ImportError:
	import util

IndentedLogger = util.IndentedLogger

logger = IndentedLogger()

class Extension:
	def __init__(self, comp):
		self.comp = comp

	def _GetId(self):
		return self.comp.par.opshortcut.eval() or self.comp.name

	@property
	def _MasterPath(self):
		master = self.comp.par.clone.eval()
		return master.path if master else self.comp.path

	def _LogEvent(self, event):
		logger.LogEvent(self.comp.path, self._GetId(), event)

	def _LogBegin(self, event):
		logger.LogBegin(self.comp.path, self._GetId(), event)

	def _LogEnd(self, event=None):
		logger.LogEnd(self.comp.path, self._GetId(), event)

	LogEvent = _LogEvent
	LogBegin = _LogBegin
	LogEnd = _LogEnd


