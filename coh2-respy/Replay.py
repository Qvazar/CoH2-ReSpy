#from PyQt5.QtCore import (QFile, QIODevice)
import Player

class NotAReplayException(Exception):
	pass

class Replay:
	@staticmethod
	def isCohReplay(buffer):
		return buffer[0x4:0xc] == b"COH2_REC"

	@staticmethod
	def readPlayers(buffer):
		pass

	@staticmethod
	def readMapName(buffer):
		len = int.from_bytes(buffer[0x108:0x10c], byteorder="big")
		return buffer[0x10c:(0x10c+len)].decode(encoding="ascii")

	@classmethod
	def fromFile(cls, filepath):
		with open(filepath, "rb") as file
			buffer = file.read()

			if !isCohReplay(buffer)
				raise NotAReplayException

			return cls(bytearray(buffer))

	def __init__(self, buffer):
		self.buffer = buffer;
		self.players = readPlayers(buffer)
		self.mapName = readMapName(buffer)

