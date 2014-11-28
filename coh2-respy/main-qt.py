from ReplayWatcher import ReplayWatcher

if __name__ == '__main__':
	def onReplayReady():
		pass

	import sys
	from PyQt5.QtWidgets import (QApplication)
	
	app = QApplication(sys.argv)

	watcher = ReplayWatcher("/home/sj/Code/CoH2-ReSpy/test/coh2-respy/data/")
	watcher.replayReady.connect(onReplayReady)
	watcher.start()

	sys.exit(app.exec_())