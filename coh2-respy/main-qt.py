from ReplayWatcher import ReplayWatcher

if __name__ == '__main__':
	import sys
	from PyQt5.QtWidgets import (QApplication)
	
	app = QApplication(sys.argv)

	watcher = ReplayWatcher("/home/sj")
	watcher.start()

	sys.exit(app.exec_())