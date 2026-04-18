import pytube, os
from pytube import extract

TOKEN = "OTA0MjcyNTk2OTE1MzM1MTc5.G6X-3t.4jDNPYbFjNFuJYZpO237rU1zRr7UYL8jaGu4tE"

MUSICPATH = "../music/youtube/"
PLAYLISTPATH = "playlists/"

MAINGUILD_ID = 878040480179433482
TESTGUILD_ID = 1032966863661043813
MY_ID = 544933092503060509

VER = "4.0"

#colors
#old 0xFF7F4D
#new, old 0xBECEFF
color = {}
PAMELLOС = 0x425EEB

LOOP1C = PAMELLOС
LOOP2C = 0xFFD562

ERRORС = 0xFF4040
INFOС = PAMELLOС

def findsong(filename: str):
	for name in os.listdir(MUSICPATH):
		if name == filename:
			return True
	return False

def findlist(filename: str):
	for name in os.listdir(PLAYLISTPATH):
		if name == filename:
			return True
	return False


class FYouTube(pytube.YouTube):
	def __init__(self, url):
		super().__init__(url=url)
		self._fast_audio = None
		self._fast_streams = []

	def strtime(self):
		h = self.length // 3600
		m = (self.length % 3600) // 60
		s = (self.length % 3600) % 60
		
		if (h): return f"{h}:{m}:{s}"
		else: return f"{m}:{s}"

	@property
	def fast_audio(self):
		self.check_availability()
		if self._fast_audio:
			return self._fast_audio

		self._fast_streams = []

		stream_manifest = extract.apply_descrambler(self.streaming_data)
		
		for stream in stream_manifest:
			video = pytube.Stream(
				stream=stream,
				monostate=self.stream_monostate,
			)
			self._fast_streams.append(video)

		self.stream_monostate.title = self.title
		self.stream_monostate.duration = self.length

		for stream in self._fast_streams:
			if (stream.type == "audio" and stream.abr == "128kbps"):
				self._fast_audio = stream
				return self._fast_audio

		return None