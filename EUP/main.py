import discord, pytube, os, random
from discord import app_commands

MAINGUILD_ID = 878040480179433482
TESTGUILD_ID = 1032966863661043813
MY_ID = 544933092503060509

#colors
PAMELLO_C = 0xFF7F4D

LOOP1_C = 0xFF535F
LOOP2_C = PAMELLO_C

ERROR_C = 0xEB4C42
INFO_C = 0x42A5EB

players = []

def ecranate(text: str):
	text = text.replace("_", "\_")
	text = text.replace("`", "\`")
	text = text.replace("~", "\~")
	text = text.replace("*", "\*")
	text = text.replace("|", "\|")
	return text

class Client(discord.Client):
	def __init__(self):
		super().__init__(intents=discord.Intents.default())
		self.synced = False

	async def on_ready(self):
		await self.wait_until_ready()
		if not self.synced:
			await tree.sync(guild=discord.Object(id=MAINGUILD_ID))
			self.synced = True
			print(f"logged in as {self.user}")

class Player():
	def __init__(self, vclient):
		self.vclient = vclient
		
		self.queue = []
		self.nq = 0

		self.loopMode = 0
		
		self.rewindTimestamp = "00:00:00"
		self.isJumped = False
		self.isActive = False
	
	def aftersong(self, none):
		self.isActive = False

		if not self.isJumped:
			if not self.loopMode:
				self.nq = 0
				if len(self.queue):
					del self.queue[0]
			elif self.loopMode == 2:
				if self.nq < len(self.queue):
					self.nq = (self.nq + 1) * ((self.nq + 1) < len(self.queue))
				else:
					self.nq = 0
		else: self.isJumped = False
		
		self.playnext(self.rewindTimestamp)
		self.rewindTimestamp = "00:00:00"

	def playnext(self, timestamp: str = "00:00:00"):
		if len(self.queue):
			if not self.isActive:
				self.vclient.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="music/youtube/" + self.queue[self.nq]["name"], before_options=f"-ss {timestamp}"), after=self.aftersong)
				self.isActive = True
		else:
			self.vclient.stop()
			self.isActive = False

	def playsection(self, sectionid: int):
		if sectionid == 0:
			self.isJumped = True
			self.vclient.stop()
			return True
		if sectionid > 0 and sectionid < len(self.queue[self.nq]["sections"]):
			self.isJumped = True
			self.rewindTimestamp = self.queue[self.nq]["sections"][sectionid]["timestamp"]
			self.vclient.stop()
			return True
		return False



	def queueAdd(self, filename: str, url: str, sections: list, user: discord.Interaction.user, n = -1):
		if n < 0 or (n >= len(self.queue)):
			self.queue.append({
				"name": filename,
				"user": user,
				"url": url,
				"sections": sections
			})
		else:
			self.queue.insert(n, {
				"name": filename,
				"user": user,
				"url": url,
				"sections": sections
			})
			self.qn += (n <= self.nq)


	def saveQueue(self, name: str, uid: int, overwrite = False):
		if not overwrite:
			for fname in os.listdir("playlists"):
				if fname == name:
					return False
		
		file = open("playlists/" + name + ".ppl", 'w', encoding="utf8")

		file.write(str(len(self.queue)) + '\n')
		for song in self.queue:
			file.write(str(len(song["sections"])) + '\n')
			for section in song["sections"]:
				file.write(section["name"] + '\n')
				file.write(section["timestamp"] + '\n')
			file.write(song["name"] + '\n')
			file.write(song["url"] + '\n')
		return True

	def loadQueue(self, name: str, user: discord.Interaction.user):
		for fname in os.listdir("playlists"):
			if fname == (name + ".ppl"):
				file = open("playlists/" + name + ".ppl", 'r', encoding="utf8")

				sections = []
				for i in range(int(file.readline()[:-1])):
					for j in range(int(file.readline()[:-1])):
						sections.append({
							"name": file.readline()[:-1],
							"timestamp": file.readline()[:-1]
						})
						sections = []
					self.queueAdd(file.readline()[:-1], file.readline()[:-1], sections, user)
				
				file.close()
				return True
		return False
	
	def clear(self):
		self.queue.clear()
		self.vclient.stop()

	def remove(self, n):
		name = None
		if (n >= 0) and (n < len(self.queue)):
			name = self.queue[n]["name"]
			del self.queue[n]
			if n < self.nq:
				self.nq -= 1
			elif n == self.nq:
				self.isJumped = True
				self.vclient.stop()
		return name

	def removerange(self, n1, n2):
		if n1 < 0: return None
		if n2 < n1: return None
		if n2 >= len(self.queue): return None
		if (n1 >= self.nq) and (self.nq <= n2): return None

		for i in range(n2 - n1):
			del self.queue[n1]
		return n2 - n1 + 1
	
	def skip(self):
		name = None
		if len(self.queue):
			name = self.queue[self.nq]["name"]
			self.vclient.stop()
		return name
	
	def jump(self, n: int):
		if n < len(self.queue):
			if not self.loopMode:
				for i in range(n):
					del self.queue[0]
			self.nq = n * bool(self.loopMode)

			self.isJumped = True
			self.vclient.stop()
		return self.queue[self.nq]["name"]
	
	def move(self, fr, to):
		if to == fr: return
		if to > fr: to, fr = fr, to

		if self.nq == fr: self.nq = to
		elif (self.nq >= to) and (self.nq < fr):
			self.nq += 1
			if self.nq == len(self.queue): self.nq = 0
		
		self.queue.insert(to, self.queue.pop(fr))

	def swap(self, n1, n2):
		if n1 == self.nq: self.nq = n2
		elif n2 == self.nq: self.nq = n1

		self.queue[n1], self.queue[n2] = self.queue[n2], self.queue[n1]
	
	def multSong(self, n, mult):
		if (n >= 0) and (n < len(self.queue)):
			if n < self.nq:
				self.nq += mult - 1
			for i in range(mult - 1):
				self.queue.insert(n, self.queue[n])
	
	def unloop(self):
		if self.nq:
			for i in range(self.nq):
				del self.queue[0]
		self.nq = 0

class ErrorEmbed(discord.Embed):
	def __init__(self, message):
		super().__init__()
		self.description = message
		self.title = "Error"
		self.color = discord.Colour(0xEB4C42)

class InfoEmbed(discord.Embed):
	def __init__(self, message):
		super().__init__()
		self.description = message
		self.color = discord.Colour(PAMELLO_C)

client = Client()
tree = app_commands.CommandTree(client)

def getPlayer(interaction: discord.Interaction):
	if len(players):
		for player in players:
			if (player.vclient.guild == interaction.guild): return player
	return None

def getVideoSections(video):
	sections = []
	try:
		for macroMarkersListRenderer in video.initial_data["engagementPanels"][1]["engagementPanelSectionListRenderer"]["content"]["macroMarkersListRenderer"]["contents"]:
			item = macroMarkersListRenderer["macroMarkersListItemRenderer"]
			times = item["timeDescription"]["simpleText"].split(":")
			times.reverse()
			sections.append({
				"name": item["title"]["simpleText"],
				"timestamp": f'{times[2] if (len(times) == 3) else "00"}:{times[1] if (len(times) >= 2) else "00"}:{times[0] if (len(times) >= 1) else "00"}'
			})
	except: pass

	return sections

def getSongHyperlink(song):
	return f"[{song['name'][:-4]}]({song['url']})"

def getTSSeconds(timestamp):
	times = timestamp.split(":")
	return int(times[0]) * 3600 + int(times[1]) * 60 + int(times[2])

@tree.command(name="ping", description="ping-pong", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def ping(interaction: discord.Interaction, test: bool = True):
	if not test: await interaction.response.send_message("pong")
	else:
		embed = discord.Embed()
		embed.set_thumbnail(url="https://media.sproutsocial.com/uploads/2017/02/10x-featured-social-media-image-size.png")
		embed.description = "test"

		await interaction.response.send_message(embed=embed)

@tree.command(name="play", description="Play song", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def play(interaction: discord.Interaction, url: str):
	player = getPlayer(interaction)
	if not player:
		if interaction.user.voice:
			players.append(Player(await interaction.user.voice.channel.connect()))
			player = players[-1]
		else:
			await interaction.response.send_message(embed=ErrorEmbed("You must be in voice channel to use this command"))
			return
	
	embed = discord.Embed()
	embed.title = "Processing..."
	
	if url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be":
		embed.description = "Getting audio info..."
		await interaction.response.send_message(embed=embed)

		video = pytube.YouTube(url)
		first = video.streams.filter(type="audio")
		first = first.first()

		for name in os.listdir("music/youtube"):
			if name == first.default_filename:
				embed.title = "Song added to queue"
				embed.description = "[" + first.default_filename[:-4] + "](" + url + ")"
				embed.colour = discord.Colour(PAMELLO_C)
				embed.set_thumbnail(url="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(video.video_id))
				await interaction.edit_original_response(embed=embed)
				break
		else:
			embed.description = "Downloading audio..."
			await interaction.edit_original_response(embed=embed)

			tStream = None

			for stream in video.streams:
				if stream.type == "audio" and stream.abr == "128kbps":
					tStream = stream
					break
			
			tStream.download("music/youtube/")
			embed.title = "Song downloaded and added to queue"
			embed.description = "[" + first.default_filename[:-4] + "](" + url + ")"
			embed.colour = discord.Colour(PAMELLO_C)
			embed.set_thumbnail(url="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(video.video_id))
			await interaction.edit_original_response(embed=embed)
		
		player.queueAdd(first.default_filename, url, getVideoSections(video), interaction.user)
	else:
		await interaction.response.send_message(embed=ErrorEmbed("Only youtube links supported"))
	player.playnext()

@tree.command(name="playnext", description="Play song next", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def playnext(interaction: discord.Interaction, url: str):
	player = getPlayer(interaction)
	if not player:
		if interaction.user.voice:
			players.append(Player(await interaction.user.voice.channel.connect()))
			player = players[-1]
		else:
			await interaction.response.send_message(embed=ErrorEmbed("You must be in voice channel to use this command"))
			return
	
	embed = discord.Embed()
	embed.title = "Processing..."

	if url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be":
		embed.description = "Getting audio info..."
		await interaction.response.send_message(embed=embed)

		video = pytube.YouTube(url)
		first = video.streams.filter(type="audio")
		first = first.first()

		for name in os.listdir("music/youtube"):
			if name == first.default_filename:
				embed.title = "Song added to queue"
				embed.description = "[" + first.default_filename[:-4] + "](" + url + ")"
				embed.colour = discord.Colour(PAMELLO_C)
				embed.set_thumbnail(url="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(video.video_id))
				await interaction.edit_original_response(embed=embed)
				break
		else:
			embed.description = "Downloading audio..."
			await interaction.edit_original_response(embed=embed)

			tStream = None

			for stream in video.streams:
				if stream.type == "audio" and stream.abr == "128kbps":
					tStream = stream
					break
			
			tStream.download("music/youtube/")
			embed.title = "Song downloaded and added to queue"
			embed.description = "[" + first.default_filename[:-4] + "](" + url + ")"
			embed.colour = discord.Colour(PAMELLO_C)
			embed.set_thumbnail(url="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(video.video_id))
			await interaction.edit_original_response(embed=embed)
		
		player.queueAdd(first.default_filename, url, getVideoSections(video), interaction.user, player.nq + bool(len(player.queue)))
	else:
		await interaction.response.send_message(embed=ErrorEmbed("Only youtube links supported"))
	player.playnext()

@tree.command(name="playnow", description="Play song imidiatly", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def playnow(interaction: discord.Interaction, url: str):
	player = getPlayer(interaction)
	if not player:
		if interaction.user.voice:
			players.append(Player(await interaction.user.voice.channel.connect()))
			player = players[-1]
		else:
			await interaction.response.send_message(embed=ErrorEmbed("You must be in voice channel to use this command"))
			return

	embed = discord.Embed()
	embed.title = "Processing..."
	
	if url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be":
		embed.description = "Getting audio info..."
		await interaction.response.send_message(embed=embed)

		video = pytube.YouTube(url)
		first = video.streams.filter(type="audio")
		first = first.first()

		for name in os.listdir("music/youtube"):
			if name == first.default_filename:
				embed.title = "Song added to queue"
				embed.description = "[" + first.default_filename[:-4] + "](" + url + ")"
				embed.colour = discord.Colour(PAMELLO_C)
				embed.set_thumbnail(url="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(video.video_id))
				await interaction.edit_original_response(embed=embed)
				break
		else:
			embed.description = "Downloading audio..."
			await interaction.edit_original_response(embed=embed)

			tStream = None

			for stream in video.streams:
				if stream.type == "audio" and stream.abr == "128kbps":
					tStream = stream
					break
			
			tStream.download("music/youtube/")
			embed.title = "Song downloaded and added to queue"
			embed.description = "[" + first.default_filename[:-4] + "](" + url + ")"
			embed.colour = discord.Colour(PAMELLO_C)
			embed.set_thumbnail(url="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(video.video_id))
			await interaction.edit_original_response(embed=embed)
		
		if len(player.queue):
			player.queueAdd(first.default_filename, url, getVideoSections(video), interaction.user, player.nq + 1)
			player.vclient.stop()
		else:
			player.queueAdd(first.default_filename, url, getVideoSections(video), interaction.user)
			player.playnext()
	else:
		await interaction.response.send_message(embed=ErrorEmbed("Only youtube links supported"))

@tree.command(name="playlist", description="Add songs from playlist in end of queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def playlist(interaction: discord.Interaction, name: str):
	player = getPlayer(interaction)
	if not player:
		if interaction.user.voice:
			players.append(Player(await interaction.user.voice.channel.connect()))
			player = players[-1]
		else:
			
			await interaction.response.send_message(embed=ErrorEmbed("You must be in voice channel to use this command"))
			return
	
	for fname in os.listdir("playlists"):
		if fname == (name + ".ppl"):
			if player.loadQueue(name, interaction.user):
				await interaction.response.send_message(embed=InfoEmbed("Songs from playlist \"**{}**\" added to queue".format(ecranate(name))))
			else:
				await interaction.response.send_message(embed=ErrorEmbed("Can`t play this playlist((("))
			player.playnext()
			break
	else:
		await interaction.response.send_message(embed=ErrorEmbed("Playlist named \"{}\" not found".format(name)))

@tree.command(name="playepisode", description="Add songs from playlist in end of queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def playepisode(interaction: discord.Interaction, episodeid: int):
	player = getPlayer(interaction)
	if player:
		if player.playsection(episodeid - 1):
			await interaction.response.send_message(embed=InfoEmbed(f"Song {getSongHyperlink(player.queue[player.nq])} rewinded to episode `{episodeid}` ([{player.queue[player.nq]['sections'][episodeid - 1]['timestamp']}]({player.queue[player.nq]['url']}&t={getTSSeconds(player.queue[player.nq]['sections'][episodeid - 1]['timestamp'])}s))"))
		else:
			await interaction.response.send_message(embed=ErrorEmbed("Invalid section ID"))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="playing", description="Write playing song name", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def playing(interaction: discord.Interaction):
	player = getPlayer(interaction)
	if player: await interaction.response.send_message(embed=InfoEmbed("Now playing `{}` - [{}]({})\nadded by **{}**".format(player.nq + 1, player.queue[player.nq]["name"][:-4], player.queue[player.nq]["url"], player.queue[player.nq]["user"].name)))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="jump", description="Jump tp song in queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def jump(interaction: discord.Interaction, qid: int, skip: bool = True):
	player = getPlayer(interaction)
	if player: await interaction.response.send_message(embed=InfoEmbed("Jumped to **{}**".format(ecranate(player.jump(qid - 1)[:-4]))))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="skip", description="Skip current song", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def skip(interaction: discord.Interaction):
	player = getPlayer(interaction)
	if player: await interaction.response.send_message(content="Song **%s** skipped" % player.skip()[:-4])
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="remove", description="Remove song by position in queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def remove(interaction: discord.Interaction, qid: int):
	player = getPlayer(interaction)
	if player:
		await interaction.response.send_message(content="Song **%s** removed" % player.remove(qid - 1)[:-4])
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="removerange", description="Remove songs by from position 1 to position 2 in queue (first pos must be smaller than second)", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def removerange(interaction: discord.Interaction, qid1: int, qid2: int):
	player = getPlayer(interaction)
	if player: await interaction.response.send_message(content="Removed **%d** songs" % player.removerange(qid1 - 1, qid2 - 1))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="swap", description="Swap two songs in queue between themselves", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def swap(interaction: discord.Interaction, qid1: int, qid2: int):
	player = getPlayer(interaction)
	if player:
		player.swap(qid1 - 1, qid2 - 1)
		await interaction.response.send_message(embed=InfoEmbed("Songs in pos **{}** and **{}** swaped".format(qid1, qid2)))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="move", description="Move song in queue to position", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def move(interaction: discord.Interaction, qfrom: int, qto: int):
	player = getPlayer(interaction)
	if player:
		player.move(qfrom - 1, qto - 1)
		await interaction.response.send_message(embed=InfoEmbed("Song from pos **{}** moved to **{}**".format(qfrom, qto)))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="queue", description="Write queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def queue(interaction: discord.Interaction):
	player = getPlayer(interaction)
	if player:
		message = "" if len(player.queue) else "Empty"
		for i in range(len(player.queue)):
			if (len(message) + len(player.queue[i]["name"]) + len(player.queue[i]["user"].name) + 22) > 3900:
				message += "   **...**"
				break
			message += "`{}` {} {}[{}]({})\n".format(
				i + 1,
				"**now >**" if player.nq == i else "-",
				"(looped) " if ((player.loopMode == 1) and (player.nq == i)) else "",
				ecranate(player.queue[i]["name"][:-4]),
				player.queue[i]["url"]
			)

			for j in range(len(player.queue[i]["sections"])):
				message += f'- - - - `{j + 1}` : [{ecranate(player.queue[i]["sections"][j]["name"])}]({player.queue[i]["url"]}&t={str(getTSSeconds(player.queue[i]["sections"][j]["timestamp"]))}s)\n'

			message += "added by **{}**\n".format(ecranate(player.queue[i]["user"].name))
		
		embed = discord.Embed()
		if player.loopMode == 1: embed.colour = discord.Colour(LOOP1_C)
		elif player.loopMode == 2: embed.colour = discord.Colour(LOOP2_C)
		embed.title = "Queue (looped)" if player.loopMode == 2 else "Queue"
		embed.description = message
		embed.set_image(url="https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(pytube.YouTube(player.queue[player.nq]["url"]).video_id))

		await interaction.response.send_message(embed=embed)
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="shuffle", description="Shuffle queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def shuffle(interaction: discord.Interaction):
	player = getPlayer(interaction)
	if player:
		csong = player.queue[player.nq]
		random.shuffle(player.queue)
		player.nq = player.queue.index(csong)
		if not player.loopMode and not player.nq: player.queue.insert(0, player.queue.pop(player.nq))
		player.nq = 0

		if len(player.queue): await interaction.response.send_message(content="Queue shuffled")
		else: await interaction.response.send_message(content="Queue is empty")
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="loop", description="Loop queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def loop(interaction: discord.Interaction, single: bool = False):
	player = getPlayer(interaction)
	if player:
		if not player.loopMode or (single + 1 == player.loopMode):
			player.loopMode = (not single) + 1
			await interaction.response.send_message(embed=InfoEmbed("Curent song looped" if single else "Queue is looped"))
		else:
			player.unloop()
			await interaction.response.send_message(embed=InfoEmbed("Queue is no more in loop"))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="clear", description="Clear queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def clear(interaction: discord.Interaction):
	player = getPlayer(interaction)
	if player:
		if len(player.queue):
			player.clear()
			await interaction.response.send_message(content="Queue is cleared")
		else: await interaction.response.send_message(content="Queue is empty")
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="mult", description="Mult song in queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def mult(interaction: discord.Interaction, qid: int, mult: int):
	player = getPlayer(interaction)
	if player:
		player.multSong(qid - 1, mult)
		await interaction.response.send_message(content="Song **{}** multiplied **{}** times".format(player.queue[qid]["name"][:-4], mult))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="pause", description="Pause player", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def pause(interaction: discord.Interaction):
	player = getPlayer(interaction)
	if player:
		await interaction.response.send_message(content="Player paused" if not player.vclient.is_paused() else "Player already paused")
		player.vclient.pause()
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="resume", description="Resume player", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def resume(interaction: discord.Interaction):
	player = getPlayer(interaction)
	if player:
		await interaction.response.send_message(content="Player resumed" if player.vclient.is_paused() else "Player already playing")
		player.vclient.resume()
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="save", description="Save songs from queue to playlist", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def save(interaction: discord.Interaction, name: str, overwrite: bool = False):
	player = getPlayer(interaction)
	if player:
		await interaction.response.send_message(embed=InfoEmbed("Songs from queue saved in playlist \"**{}**\"".format(name) if player.saveQueue(name, overwrite) else "Playlist \"**{}**\" already exists".format(name)))
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

@tree.command(name="exit", description="Kill player", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def exit(interaction: discord.Interaction):
	player = getPlayer(interaction)
	if player:
		if len(player.queue):
			player.clear()
		await player.vclient.disconnect()
		players.remove(player)
		await interaction.response.send_message(content="Player killed :skull:")
	else: await interaction.response.send_message(embed=ErrorEmbed("Can`t find players in this guild"))

client.run("OTA0MjcyNTk2OTE1MzM1MTc5.G6X-3t.4jDNPYbFjNFuJYZpO237rU1zRr7UYL8jaGu4tE")
