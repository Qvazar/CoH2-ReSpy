import os
from PyQt5.QtCore import (pyqtSignal, QObject, QFileSystemWatcher)
from Replay import Replay

class ReplayWatcher(QObject):

	replayReady = pyqtSignal(Replay)

	def __init__(self, replayDirectory):
		QObject.__init__(self)
		self.replayPath = replayDirectory
		self.replayFilePath = os.path.join(replayDirectory,  "temp.rec")
		self._watcher = QFileSystemWatcher()

	def start(self):
		self._startDirWatch()
		self._startFileWatch()

	def stop(self):
		self._watcher.removePath(self.directory)

	def _startDirWatch(self):
		watcher = self._watcher
		
		if watcher.addPath(self.replayPath):
			watcher.directoryChanged.connect(self._onDirectoryChanged)
		else:
			raise FileNotFoundError(self.replayPath)
		
	def _startFileWatch(self):
		watcher = self._watcher
		
		if watcher.addPath(self.replayFilePath):
			watcher.fileChanged.connect(self._onFileChanged)

	def _onDirectoryChanged(self, dirpath):
		if len(self._watcher.files()) == 0:
			self._startFileWatch()

	def _onFileChanged(self, filepath):
		print("FileChanged: %s" % filepath)
		try:
			replay = Replay.fromFile(filepath)
			self.replayReady.emit(replay)
		except:
			#TODO: Logging
			pass
