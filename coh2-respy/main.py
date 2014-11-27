import sys
from Replay import Replay

replay = Replay.fromFile("../test/27508.relicscrubs.rec")

print("Map name: %s" % replay.mapName)
print("Seekable: %s" % replay.buffer.seekable())