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

			return cls(buffer)

	def __init__(self, buffer):
		self.buffer = buffer;

		def skip(len):
			buffer.seek(len, io.SEEK_CUR)

		def readAsciiString():
			len = readInt()
			return buffer.read(len).decode(encoding="ascii")

		def readUtfString():
			len = readInt()
			return buffer.read(len).decode(encoding="utf-16")

		def readFloat():
			import struct
			return struct.unpack_from("<f", buffer.read(4))[0]

		def readInt():
			return int.from_bytes(buffer.read(4), byteorder="little")

		skip(0x108)
		self.mapName = readAsciiString().rpartition("\\")[2]

		skip(0xcf)
		#skip territory points (why are they there?)
		while buffer.peek(0x8) != b"FOLDINFO":
			print(readFloat()) # x-pos?
			print(readFloat()) # y-pos?
			print(readAsciiString())

		#self.mapName = self.readMapName(buffer)

