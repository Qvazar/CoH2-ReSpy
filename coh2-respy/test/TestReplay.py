from Replay import Replay
import unittest

class TestReplay(unittest.TestCase):
	
	def setUp(self):
		pass

	def testInvalidReplay(self):
		with self.assertRaises(Exception):
			Replay.fromFile("test/data/not-a-replay.rec")

	def testMapName(self):
		replay = Replay.fromFile("test/data/27508.relicscrubs.rec")

if __name__ == '__main__':
    unittest.main()