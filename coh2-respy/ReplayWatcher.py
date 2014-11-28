from PyQt5.QtCore import (pyqtSignal, QObject, QFileSystemWatcher)
from Replay import Replay

class ReplayWatcher(QObject):

	replayReady = pyqtSignal(Replay)

	def __init__(self, replayDirectory):
		QObject.__init__(self)
		self.directory = replayDirectory
		self._watcher = QFileSystemWatcher()

	def start(self):
		watcher = _self.watcher

		if not watcher.addPath(self.directory):
			raise FileNotFoundError

		watcher.directoryChanged.connect(self._onDirectoryChanged)
		print(watcher.directories())

	def stop(self):
		self._watcher.removePath(self.directory)

	def _onDirectoryChanged(self, filepath):
		print("DirectoryChanged: %s" % filepath)
		try:
			replay = Replay.fromFile(filepath)
			self.replayReady.emit(replay)
		except:
			#TODO: Logging
			pass
