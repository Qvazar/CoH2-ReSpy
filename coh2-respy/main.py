import sys
from Replay import Replay

replay = Replay.fromFile("test/data/27508.relicscrubs.rec")

print("Replay: %s" % replay.__dict__)
print("Seekable: %s" % replay.buffer.seekable())