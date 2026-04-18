import discord, pytube, os, random
from header import MUSICPATH, PLAYLISTPATH, FYouTube, findsong, findlist

def ecranate(text: str):
	text = text.replace("_", "\_")
	text = text.replace("`", "\`")
	text = text.replace("~", "\~")
	text = text.replace("*", "\*")
	text = text.replace("|", "\|")
	return text


class Song():
	def __init__(self, name: str, user: discord.User, ytid: str):
		self.name = name
		self.user = user
		self.ytid = ytid

		self.episodes = []
	
	def geturl(self):
		return "https://youtu.be/" + self.ytid
	
	def geteurl(self, eid: int):
		times = self.episodes[eid]["timestamp"].split(":")
		return "https://youtu.be/" + self.ytid + "&t=" + str(int(times[0]) * 3600 + int(times[1]) * 60 + int(times[2])) + "s"

	def getimageurl(self):
		return "https://i.ytimg.com/vi/" + self.ytid + "/maxresdefault.jpg"
	
	def gethyperlink(self):
		return f"[{ecranate(self.name)}]({self.geturl()})"
	
	def searchepisodes(self, video: FYouTube = None):
		if not video: video = FYouTube(self.geturl())
		try:
			for macroMarkersListRenderer in video.initial_data["engagementPanels"][1]["engagementPanelSectionListRenderer"]["content"]["macroMarkersListRenderer"]["contents"]:
				item = macroMarkersListRenderer["macroMarkersListItemRenderer"]
				self.episodes.append({
					"name": item["title"]["simpleText"],
					"timestamp": f'{("0:" if (len(item["timeDescription"]["simpleText"].split(":")) == 2) else "") + item["timeDescription"]["simpleText"]}'
				})
			return len(self.episodes)
		except:
			return 0


class Player():
	def __init__(self, vclient: discord.VoiceClient):
		self.vclient = vclient
		
		self.queue = []
		self.qn = 0

		self.loopmode = 0
		
		self.backto = -1
		self.startfrom = "00:00:00"
		self.isjumped = False
		self.isactive = False

	def aftersong(self, none):
		self.isactive = False

		if not self.isjumped:
			if self.backto > -1:
				self.qn = self.backto
				self.backto = -1
			elif not self.loopmode:
				if self.queue:
					del self.queue[0]
			elif self.loopmode == 2:
				self.qn += 1

				if self.qn == len(self.queue):
					self.qn = 0
		else: self.isjumped = False

		self.playnext()
		self.startfrom = "00:00:00"

	def playnext(self):
		if len(self.queue):
			if not self.isactive:
				self.vclient.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="../music/youtube/" + self.queue[self.qn].name + ".mp4", before_options=f"-ss {self.startfrom}"), after=self.aftersong)
				self.isactive = True
		else:
			self.vclient.stop()
			self.isactive = False
	
	def playepisode(self, eid: int):
		if eid == 0:
			self.isjumped = True
			self.vclient.stop()
			return True
		if eid > 0 and eid < len(self.queue[self.qn].episodes):
			self.isjumped = True
			self.startfrom = self.queue[self.qn].episodes[eid]["timestamp"]
			self.vclient.stop()
			return True
		return False

	def queueinsert(self, song: Song, qid: int = -1):
		if qid < 0 or qid >= len(self.queue):
			self.queue.append(song)
		else:
			if qid <= self.qn: self.qn += 1
			self.queue.insert(qid, song)
	
	def savequeue(self, name: str, overwrite: bool = False, isprivate: bool = False, privateid: int = 0):
		if findlist(name):
			if overwrite:
				file = open(PLAYLISTPATH + name, 'r', encoding="utf8")
				
				ver = file.readline()[:-1]
				if ver != "ver-4.0": return -2

				fprivateid = int(file.readline()[:-1])
				if fprivateid and fprivateid != privateid: return -3

				file.close()
			else: return -1


		file = open(PLAYLISTPATH + name, "w", encoding="utf8")

		file.write("ver-4.0\n")
		file.write(str(privateid * isprivate) + '\n')
		file.write(str(len(self.queue)) + '\n')

		for song in self.queue:
			file.write(song.name + '\n')
			file.write(song.ytid + '\n')
			file.write(str(len(song.episodes)) + '\n')
			for episode in song.episodes:
				file.write(episode["name"] + '\n')
				file.write(episode["timestamp"] + '\n')
		
		file.close()

		return 0
	def loadqueue(self, name: str, user: discord.User | discord.Member, useprivate: bool = True):
		count = 0
		privateid = 0

		if name != "all":
			if findlist(name):
				file = open(PLAYLISTPATH + name, 'r', encoding="utf8")
				
				ver = file.readline()[:-1]
				if ver != "ver-4.0": return -2
				file.readline()

				for i in range(int(file.readline()[:-1])):
					song = Song(file.readline()[:-1], user, file.readline()[:-1])
					for j in range(int(file.readline()[:-1])):
						song.episodes.append({
							"name": file.readline()[:-1],
							"timestamp": file.readline()[:-1]
						})
					self.queueinsert(song)
					count += 1
				
				file.close()
			else:
				return -1

		else:
			for fname in os.listdir(PLAYLISTPATH):
				file = open("playlists/" + fname, 'r', encoding="utf8")

				ver = file.readline()[:-1]
				if ver != "ver-4.0": return -2
				file.readline()

				for i in range(int(file.readline()[:-1])):
					song = Song(file.readline()[:-1], user, file.readline()[:-1])
					for j in range(int(file.readline()[:-1])):
						song.episodes.append({
							"name": file.readline()[:-1],
							"timestamp": file.readline()[:-1]
						})
					self.queueinsert(song)
					count += 1
				
				file.close()

		return count

	def shuffle(self):
		if not self.queue: return False

		csong = self.queue[self.qn]
		random.shuffle(self.queue)
		self.qn = self.queue.index(csong)

		if not self.loopmode and self.qn:
			self.queue.insert(0, self.queue.pop(self.qn))
			self.qn = 0
		
		return True

	def clear(self):
		self.queue.clear()
		self.vclient.disconnect()
	
	def skip(self):
		if self.queue:
			self.vclient.stop()
			return True
		return False
	def remove(self, qid: int):
		if qid > -1 and qid < len(self.queue):
			del self.queue[qid]
			
			if qid < self.qn:
				if self.qn: self.qn -= 1
			elif qid == self.qn:
				if len(self.queue): self.isjumped = True
				self.vclient.stop()
			
			return True
		return False
	def removerange(self, qid1: int, qid2: int):
		if (qid1 > qid2): qid1, qid2 = qid2, qid1

		if (qid1 >= 0) and (qid2 < len(self.queue)):
			for i in range(qid2 - qid1 + 1):
				del self.queue[qid1]
			
			if qid2 < self.qn:
				self.qn -= qid2 - qid1 + 1
			elif qid1 <= self.qn:
				self.qn = qid1 - bool(qid1)
				self.isjumped = True
				self.vclient.stop()

			return True
		return False

	def move(self, qid1: int, qid2: int):
		if ((qid1 != qid2) and
			(qid1 >= 0) and
			(qid2 >= 0) and
			(qid1 < len(self.queue)) and
			(qid2 < len(self.queue))
			):
			if self.qn and qid1 <= self.qn: self.qn -= 1
			if qid2 <= self.qn: self.qn += 1
			self.queueinsert(self.pop(qid1), qid2)
			return True
		return False
	def swap(self, qid1: int, qid2: int):
		if self.qn == qid1: self.qn = qid2
		elif self.qn == qid2: self.qn = qid1

		if ((qid1 != qid2) and
			(qid1 >= 0) and
			(qid2 >= 0) and
			(qid1 < len(self.queue)) and
			(qid2 < len(self.queue))):
			self.queue[qid1], self.queue[qid2] = self.queue[qid2], self.queue[qid1]
			return True
		return False
	
	def jump(self, qid: int):
		if qid >= 0 and qid < len(self.queue):
			if not self.loopmode:
				for i in range(qid):
					del self.queue[0]
			self.qn = qid * bool(self.loopmode)

			self.isjumped = True
			self.vclient.stop()
			return True
		return False
	def step(self, qid: int):
		if qid >= 0 and qid < len(self.queue):
			self.backto = self.qn
			self.qn = qid

			self.isjumped = True
			self.vclient.stop()
			return True
		return False

	def loop(self, mode: int):
		if self.loopmode == mode: return False
		
		if self.loopmode and not mode:
			if self.qn:
				for i in range(self.qn):
					self.queue.append(self.queue.pop(0))
			self.qn = 0
			self.loopmode = 0
		else: self.loopmode = mode
		
		return True