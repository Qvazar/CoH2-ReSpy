import io
import dateutil.parser
import pdb
from Player import Player

class InvalidFileException(Exception):
	def __init__(self): self.message = "File does not seem to be a CoH2 replay.";

class Replay:

	@classmethod
	def fromFile(cls, filepath):
		with open(filepath, "rb") as file:
			contents = file.read()

			buffer = io.BufferedRandom(io.BytesIO(contents))

			return cls.fromBuffer(buffer)

	@classmethod
	def fromBuffer(cls, buffer):
		version 		= None
		gameType 		= None
		time			= None
		modName 		= None
		mapFile 		= None
		mapName 		= None
		mapDescription 	= None
		mapWidth 		= None
		mapHeight 		= None
		mapSeason 		= None
		playerCount 	= None
		players 		= []
		winCondition 	= None
		gameDuration 	= 0

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


		def readAsciiString(len = -1):
			if len == -1: len = readUInt32()
			return buffer.read(len).decode(encoding="ascii")

		def readUtfZString():
			b = bytearray()

			b += buffer.read(2)

			while int.from_bytes(b[-2:-1], byteorder="little", signed=False) != 0:
				b += buffer.read(2)
			
			b = b[:-2]

			return b.decode(encoding="utf-16")

		def readUtfString(len = -1):
			if len == -1: len = readUInt32() * 2 # 2 bytes per utf-16 character
			return buffer.read(len).decode(encoding="utf-16")

		def readFloat():
			import struct
			return struct.unpack_from("<f", buffer.read(4))[0]

		def readUInt16():
			return int.from_bytes(buffer.read(2), byteorder="little", signed=False)

		def readUInt32():
			return int.from_bytes(buffer.read(4), byteorder="little", signed=False)

		def readUInt64():
			return int.from_bytes(buffer.read(8), byteorder="little", signed=False)

		def parseChunky():
			if buffer.read(12) != b"Relic Chunky":
				raise InvalidFileException

			skip(0x4)

			if readUInt32() != 3: return False

			skip(0x4)
			skip(readUInt32() - 28)

			while parseChunk(): pass

			return True

		def parseChunk():
			nonlocal modName
			nonlocal mapFile
			nonlocal mapName
			nonlocal mapDescription
			nonlocal mapWidth
			nonlocal mapHeight
			nonlocal mapSeason
			nonlocal playerCount
			nonlocal players
			nonlocal winCondition

			chunkType = readAsciiString(8)
			if not chunkType[0:4] in ("FOLD", "DATA"):
				skip(-8)
				return False

			chunkVersion = readUInt32()
			chunkLength = readUInt32()
			chunkNameLength = readUInt32()
			skip(8)
			chunkName = readAsciiString(chunkNameLength)
			startIndex = buffer.tell()

			if chunkType[0:4] == "FOLD":
				while buffer.tell() < startIndex + chunkLength:
					parseChunk()

			if chunkType == "DATASDSC" and chunkVersion == 0x7e3:
				skip(12)
				skip(6 + 2 * readUInt32())

				#Not visible in this version
				#modName = readAsciiString()
				mapFile = readAsciiString()

				skip(16)

				mapName = readUtfString()

				skip(4)

				mapDescription = readUtfString()

				skip(4)

				mapWidth = readUInt32()
				mapHeight = readUInt32()

				#skip(47)

				#mapSeason = readAsciiString()

			if chunkType == "DATADATA" and chunkVersion == 0x17 and False: #TODO
				skip(18)

				playerCount = readUInt32()
				for i in range(playerCount):
					players.append(parsePlayer())

				skip(90)
				winCondition = readAsciiString()

			buffer.seek(startIndex + chunkLength)
			return True

		def parsePlayer():
			skip(1)

			playerName = readUtfString()
			teamId = readUInt32()
			factionId = readAsciiString()

			skip(8)

			loadout = readAsciiString() #Is it loadout? "default" in file

			# TODO Find the damn index of SteamID
			
			skip(0x50)

			steamId = readUInt64()

			skip(4)

			commanderIds = []

			for i in range(3):
				commanderIds.append(readUInt32())

			skip(4)

			bulletinIds = []

			for i in range(3):
				bulletinId = readUInt32()
				if bulletinId !=0xffffffff:
					bulletinIds.append(bulletinId)

			skip(4)

			print(playerName)
			print(teamId)
			print(factionId)
			print(loadout)
			print(steamId)
			print(commanderIds)
			print(bulletinIds)

			bulletins = []

			for i in range(readUInt32()):
				bulletins.append(readAsciiString())
				skip(4)

			skip(9)

			return Player(playerName, teamId, factionId, steamId, commanderIds, bulletinIds, bulletins)

		def parseData():
			while parseTick(): pass

		def parseTick():
			nonlocal gameDuration

			skip(4)
			if len(buffer.read(1)) == 0:
				return False
			else:
				skip(-1)

			tickSize = readUInt32()
			if tickSize:
				skip(tickSize)
				gameDuration += 1
				return True
			else:
				return False

		skip(0x2)
		version = readUInt16()

		gameType = readAsciiString(8)
		if gameType != "COH2_REC":
			raise InvalidFileException

		gameTimeIndex = buffer.tell()
		gameTime = dateutil.parser.parse(readUtfZString())

		#skipToPattern(b"DATASDSC")
		#skip(0x30)
		#mapName = readAsciiString().rpartition("\\")[2]
		#print("mapName: %s" % mapName)

		buffer.seek(0x4c, io.SEEK_SET)
		parseChunky()
		parseChunky()

		parseData()

		"""skip(0xcf)
		#skip territory points (why are they there?)
		while buffer.peek(0x8) != b"FOLDINFO":
			print(readFloat()) # x-pos?
			print(readFloat()) # y-pos?
			print(readAsciiString())
		"""


		return cls(buffer, version, gameType, gameTimeIndex, gameTime, modName, mapFile, mapName, mapDescription, mapWidth, mapHeight, mapSeason, playerCount, players, winCondition, gameDuration)


	def __init__(self, buffer, version, gameType, gameTimeIndex, gameTime, modName, mapFile, mapName, mapDescription, mapWidth, mapHeight, mapSeason, playerCount, players, winCondition, gameDuration):
		self.buffer 		= buffer
		self.version 		= version 		
		self.gameType 		= gameType
		self.gameTimeIndex	= gameTimeIndex
		self.gameTime		= gameTime
		self.modName 		= modName 		
		self.mapFile 		= mapFile 		
		self.mapName 		= mapName 		
		self.mapDescription	= mapDescription
		self.mapWidth 		= mapWidth 		
		self.mapHeight 		= mapHeight 		
		self.mapSeason 		= mapSeason 		
		self.playerCount 	= playerCount 	
		self.players 		= players 		
		self.winCondition 	= winCondition 
		self.gameDuration 	= gameDuration 

	def convertGameTimeToIsoFormat(self):
		buffer = self.buffer
		timeIndex = self.gameTimeIndex
		strIndex = timeIndex + 4

		isoTimeStr = self.gameTime.isoformat(sep = ' ')
		oldStrLen = int.from_bytes(buffer[timeIndex:strIndex], byteorder="little", signed=False)

		buffer[timeIndex:strIndex] = len(isoTimeStr).to_bytes(4, byteorder="little", signed=False)
		buffer[strIndex:strIndex + oldStrLen * 2] = isoTimeStr.encode(encoding="utf-16")
