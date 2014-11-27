#from PyQt5.QtCore import (QFile, QIODevice)
import io
import Player

class Replay:
	class NotAReplayException(Exception):
		pass

	@staticmethod
	def isCohReplay(buffer):
		return buffer[0x4:0xc] == b"COH2_REC"

	@staticmethod
	def readPlayers(buffer):
		pass

	@classmethod
	def fromFile(cls, filepath):
		with open(filepath, "rb") as file:
			contents = file.read()

			if not cls.isCohReplay(contents):
				raise NotAReplayException

			buffer = io.BufferedRandom(io.BytesIO(contents))
			#buffer.write(contents)
			buffer.seek(0)

			return cls.fromBuffer(buffer)

	@classmethod
	def fromBuffer(cls, buffer):
		def skip(len):
			buffer.seek(len, io.SEEK_CUR)

		def skipToPattern(pattern):
			i = 0
			while True:
				c = buffer.read(1)
				if len(c) == 0: return

				if c[0] == pattern[i]:
					if i == len(pattern) - 1: #Match found!
						return
					else:
						i += 1
				else:
					i = 0


		def readAsciiString():
			len = readInt()
			return buffer.read(len).decode(encoding="ascii")

		def readUtfString():
			len = readInt() * 2 # 2 bytes per utf-16 character
			return buffer.read(len).decode(encoding="utf-16")

		def readFloat():
			import struct
			return struct.unpack_from("<f", buffer.read(4))[0]

		def readInt():
			return int.from_bytes(buffer.read(4), byteorder="little")

		skipToPattern(b"DATASDSC")
		skip(0x30)
		mapName = readAsciiString().rpartition("\\")[2]
		#print("mapName: %s" % mapName)

		"""skip(0xcf)
		#skip territory points (why are they there?)
		while buffer.peek(0x8) != b"FOLDINFO":
			print(readFloat()) # x-pos?
			print(readFloat()) # y-pos?
			print(readAsciiString())
		"""

		skipToPattern(b"DATADATA")
		skip(0x2b)
		player1Name = readUtfString()
		skip(0x4)
		player1Faction = readAsciiString()
		skip(0x8)
		player1Loadout = readAsciiString()
		skip(0xf2)
		player2Name = readUtfString()
		skip(0x4)
		player2Faction = readAsciiString()
		skip(0x8)
		player2Loadout = readAsciiString()

		return cls(buffer, mapName)


	def __init__(self, buffer, mapName):
		self.buffer = buffer
		self.mapName = mapName
