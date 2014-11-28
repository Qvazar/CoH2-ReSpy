from PyQt5.QtCore import (pyqtSignal, QObject, QFile, QFileSystemWatcher)
from Replay import Replay

class ReplayWatcher(QObject):

	replayReady = pyqtSignal(Replay)

	def __init__(self, replayDirectory):
		QObject.__init__(self)
		self.directory = replayDirectory
		self._watcher = None

	def start(self):
		watcher = QFileSystemWatcher()

		if not watcher.addPath(self.directory):
			raise FileNotFoundError

		watcher.directoryChanged.connect(self._onDirectoryChanged)
		print(watcher.directories())

		self._watcher = watcher

	def stop(self):
		self._watcher.removePath(self.directory)
		self._watcher = None

	def _onDirectoryChanged(self, filepath):
		try:
			replay = Replay.fromFile(filepath)
			self.replayReady.emit(replay)
		except:
			#TODO: Logging
			pass
