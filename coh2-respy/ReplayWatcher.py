from PyQt5.QtCore import (QFile, QFileSystemWatcher)

class ReplayWatcher:
	def __init__(self, replayDirectory):
		self.directory = replayDirectory
		self._watcher = None

	def start(self):
		replayFilePath = self.directory + "/temp.rec"
		watcher = QFileSystemWatcher()

		if not watcher.addPath(replayFilePath):
			raise Error

		watcher.fileChanged.connect(self._onFileChanged)

		self._watcher = watcher

	def stop(self):
		replayFilePath = self.directory + "/temp.rec"
		self._watcher.removePath(replayFilePath)
		self._watcher = None

	def _onFileChanged(self, filepath):
		file = FileIO(filepath)
