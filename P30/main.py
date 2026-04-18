import discord, os, random, helplist, pytube, threading, time
from discord import app_commands
from pytube import extract

MAINGUILD_ID = 878040480179433482
TESTGUILD_ID = 1032966863661043813
MY_ID = 544933092503060509

#colors
#old 0xFF7F4D
#new, old 0xBECEFF
PAMELLO_C = 0xA7BEFF

LOOP1_C = 0xFF535F
LOOP2_C = PAMELLO_C

ERROR_C = 0xEB4C42
INFO_C = PAMELLO_C

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

class IEmbed(discord.Embed):
	def __init__(self, text):
		super().__init__()
		self.description = text
		self.color = INFO_C
class EEmbed(discord.Embed):
	def __init__(self, text):
		super().__init__()
		self.title = "Error"
		self.description = text
		self.color = ERROR_C


class Song():
	def __init__(self, name: str, user: discord.User, ytid: str):
		self.name = name
		self.user = user
		self.ytid = ytid

		self.episodes = []
	
	def getURL(self):
		return "https://youtu.be/" + self.ytid
	
	def getETimeURL(self, eid: int):
		times = self.episodes[eid]["timestamp"].split(":")
		return "https://youtu.be/" + self.ytid + "&t=" + str(int(times[0]) * 3600 + int(times[1]) * 60 + int(times[2])) + "s"

	def getImageURL(self):
		return "https://i.ytimg.com/vi/" + self.ytid + "/maxresdefault.jpg"
	
	def getHyperlink(self):
		return f"[{ecranate(self.name)}]({self.getURL()})"
	
	def searchEpisodes(self, video = None):
		if not video: video = pytube.YouTube(self.getURL())
		try:
			for macroMarkersListRenderer in video.initial_data["engagementPanels"][1]["engagementPanelSectionListRenderer"]["content"]["macroMarkersListRenderer"]["contents"]:
				item = macroMarkersListRenderer["macroMarkersListItemRenderer"]
				self.episodes.append({
					"name": item["title"]["simpleText"],
					"timestamp": f'{("0:" if (len(item["timeDescription"]["simpleText"].split(":")) == 2) else "") + item["timeDescription"]["simpleText"]}'
				})
			return True
		except:
			return False

class Player():
	def __init__(self, vclient):
		self.vclient = vclient
		
		self.queue = []
		self.nq = 0

		self.loopMode = 0
		
		self.leapto = -1
		self.startfrom = "00:00:00"
		self.isJumped = False
		self.isActive = False

	def aftersong(self, none):
		self.isActive = False

		if not self.isJumped:
			if self.leapto >= 0:
				self.nq = self.leapto
				self.leapto = -1
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
		
		self.playnext()
		self.startfrom = "00:00:00"

	def playnext(self):
		if len(self.queue):
			if not self.isActive:
				self.vclient.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="../music/youtube/" + self.queue[self.nq].name + ".mp4", before_options=f"-ss {self.startfrom}"), after=self.aftersong)
				self.isActive = True
		else:
			self.vclient.stop()
			self.isActive = False

	def playEpisode(self, eid: int):
		if eid == 0:
			self.isJumped = True
			self.vclient.stop()
			return True
		if eid > 0 and eid < len(self.queue[self.nq].episodes):
			self.isJumped = True
			self.startfrom = self.queue[self.nq].episodes[eid]["timestamp"]
			self.vclient.stop()
			return True
		return False
	
	def queueAdd(self, song: Song, n: int = -1):
		if n < 0 or n >= len(self.queue):
			self.queue.append(song)
		else:
			if n <= self.nq: self.nq += 1
			self.queue.incert(n, song)

	def saveQueue(self, name: str, overwrite = False):
		if name == "all": return False
		
		if not overwrite:
			for fname in os.listdir("playlists"):
				if fname == name:
					return False
		
		file = open("playlists/" + name, 'w', encoding="utf8")

		file.write("ver-3.0\n")
		file.write(str(len(self.queue)) + '\n')
		for song in self.queue:
			file.write(song.name + '\n')
			file.write(song.ytid + '\n')
			file.write(str(len(song.episodes)) + '\n')
			for episode in song.episodes:
				file.write(episode["name"] + '\n')
				file.write(episode["timestamp"] + '\n')
		
		file.close()
		return True

	def loadQueue(self, name: str, user: discord.Interaction.user):
		count = 0
		for fname in os.listdir("playlists"):
			if name != "all":
				if fname == name:
					file = open("playlists/" + name, 'r', encoding="utf8")

					for i in range(int(file.readline()[:-1])):
						song = Song(file.readline()[:-1], user, file.readline()[:-1])
						for j in range(int(file.readline()[:-1])):
							song.episodes.append({
								"name": file.readline()[:-1],
								"timestamp": file.readline()[:-1]
							})
						self.queueAdd(song)
					
					file.close()
					return 1
			else:
				file = open("playlists/" + fname, 'r', encoding="utf8")

				for i in range(int(file.readline()[:-1])):
					song = Song(file.readline()[:-1], user, file.readline()[:-1])
					for j in range(int(file.readline()[:-1])):
						song.episodes.append({
							"name": file.readline()[:-1],
							"timestamp": file.readline()[:-1]
						})
					self.queueAdd(song)
					count += 1
				
				file.close()
		
		return count

	def clear(self):
		self.queue.clear()
		self.vclient.stop()

	def remove(self, n):
		song = None
		if (n >= 0) and (n < len(self.queue)):
			song = self.queue[n]
			del self.queue[n]
			if n < self.nq:
				self.nq -= 1
			elif n == self.nq:
				self.isJumped = True
				self.vclient.stop()
		return song
	
	def removerange(self, n1, n2):
		if (n1 > n2): n1, n2 = n2, n1

		if (n1 >= 0) and (n2 < len(self.queue)):
			for i in range(n2 - n1 + 1):
				print(n1)
				del self.queue[n1]
			
			if n2 < self.nq:
				self.nq -= n2 - n1 + 1
			elif n1 <= self.nq:
				self.nq = n1 - bool(n1)
				self.isJumped = True
				self.vclient.stop()

			return True
		return False
	
	def move(self, n1, n2):
		if ((n1 != n2) and
			(n1 >= 0) and
			(n2 >= 0) and
			(n1 < len(self.queue)) and
			(n2 < len(self.queue))):
			self.queueAdd(self.pop(n1), n2)
			return True
		return False
	
	def swap(self, n1, n2):
		if self.nq == n1: self.nq = n2
		elif self.nq == n2: self.nq = n1

		if ((n1 != n2) and
			(n1 >= 0) and
			(n2 >= 0) and
			(n1 < len(self.queue)) and
			(n2 < len(self.queue))):
			self.queue[n1], self.queue[n2] = self.queue[n2], self.queue[n1]
			return True
		return False

	def multSong(self, n, mult):
		if (n >= 0) and (n < len(self.queue)):
			if n < self.nq:
				self.nq += mult - 1
			for i in range(mult - 1):
				self.queue.insert(n, self.queue[n])
			return True
		return False

	def jump(self, n: int):
		if n < len(self.queue):
			if not self.loopMode:
				for i in range(n):
					del self.queue[0]
			self.nq = n * bool(self.loopMode)

			self.isJumped = True
			self.vclient.stop()
		return self.queue[self.nq]
	
	def leap(self, n: int):
		if n < len(self.queue):
			self.leapto = self.nq
			self.nq = n

			self.isJumped = True
			self.vclient.stop()
		return self.queue[self.nq]
	
	def skip(self):
		song = None
		if len(self.queue):
			song = self.queue[self.nq]
			self.vclient.stop()
		return song
	
	def unloop(self):
		if self.nq:
			for i in range(self.nq):
				self.queue.append(self.queue.pop(0))
		self.nq = 0
		self.loopMode = 0

def findPlayer(interaction: discord.Interaction):
	if len(players):
		for player in players:
			if (player.vclient.guild == interaction.guild): return player
	return None

def fastAudioStream(ptvideo: pytube.YouTube):
	stream_manifest = extract.apply_descrambler(ptvideo.streaming_data)
	fmt_streams = []

	for stream in stream_manifest:
		video = pytube.Stream(
			stream=stream,
			monostate=ptvideo.stream_monostate,
		)
		fmt_streams.append(video)

	ptvideo.stream_monostate.title = ptvideo.title
	ptvideo.stream_monostate.duration = ptvideo.length

	for stream in fmt_streams:
		if (stream.type == "audio"
			and stream.abr == "128kbps"
		): return stream
	
	return None

client = Client()
tree = app_commands.CommandTree(client)

def link(url, label=None):
    if label is None: 
        label = url
    parameters = ''

    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, url, label)

RESET = '\033[0m'
def color(red, green, blue):
	return f'\033[38;2;{red};{green};{blue}m'

def mainloop():
	while not client.synced:
		time.sleep(1)
	print("cready")
	while True:
		c = input().split()
		
		if c[0] == "players":
			if not len(players):
				print("Can`t find any players")
				continue
			for player in players:
				print(player.vclient.guild.id, ":", player.vclient.guild.name)
		elif c[0] == "queue":
			for i in range(len(players)):
				print(f"{color(99, 99, 255)}{i}{RESET} : {color(99, 99, 99)}{players[i].vclient.guild.id}{RESET} {players[i].vclient.guild.name}")
			if len(players): n = input("> ")
			else:
				print("Can`t find any players")
				continue

			for j in range(len(players[int(n)].queue)):
				print(f"{color(255, 99, 99)}{'now ' if n == players[i].nq else ''}{color(99, 99, 99)}{j}{RESET} - {color(99, 99, 255)}{link(players[i].queue[j].getURL(), players[i].queue[j].name)}{RESET}")
				print(f"added by {color(255, 213, 98)}{players[i].queue[j].user.name}{RESET}")



@tree.command(name="help", description="ping-pong", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.choices(command=[
	app_commands.Choice(name="commands", value=0),
	app_commands.Choice(name="play", value=1),
	app_commands.Choice(name="playing", value=2),
	app_commands.Choice(name="playlist", value=3),
	app_commands.Choice(name="playepisode", value=4),
	app_commands.Choice(name="queue", value=5),
	app_commands.Choice(name="jump", value=6),
	app_commands.Choice(name="skip", value=7),
	app_commands.Choice(name="swap", value=8),
	app_commands.Choice(name="move", value=9),
	app_commands.Choice(name="mult", value=10),
	app_commands.Choice(name="remove", value=11),
	app_commands.Choice(name="removerange", value=12),
	app_commands.Choice(name="shuffle", value=13),
	app_commands.Choice(name="clear", value=14),
	app_commands.Choice(name="loop", value=15),
	app_commands.Choice(name="pause", value=16),
	app_commands.Choice(name="resume", value=17),
	app_commands.Choice(name="exit", value=18),
	app_commands.Choice(name="save", value=19),
	app_commands.Choice(name="ping", value=20),
])
async def help(interaction: discord.Interaction, command: app_commands.Choice[int]):
	embed = discord.Embed()
	embed.title = "Help"
	embed.description = helplist.commands[command.name]

	embed.color = PAMELLO_C
	await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="ping", description="ping-pong", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def ping(interaction: discord.Interaction):
	await interaction.response.send_message("pong", ephemeral=True)

@tree.command(name="play", description="Play song from YouTube", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	url = "YouTube link"
)
async def play(interaction: discord.Interaction, url: str):
	player = findPlayer(interaction)
	if not player:
		if interaction.user.voice:
			players.append(Player(await interaction.user.voice.channel.connect()))
			player = players[-1]
		else:
			await interaction.response.send_message(embed=EEmbed("You must be in voice channel to use this command"), ephemeral=True)
			return
	
	embed = discord.Embed()
	embed.title = "Processing..."
	
	if url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be":
		embed.description = "Getting audio info..."
		await interaction.response.send_message(embed=embed)

		video = pytube.YouTube(url)
		astream = fastAudioStream(video)

		song = Song(astream.default_filename[:-4], interaction.user, video.video_id)
		
		if song.searchEpisodes(video):
			embed.set_footer(text="song have " + str(len(song.episodes)) + " episodes")
		else:
			h = video.length // 3600
			m = (video.length % 3600) // 60
			s = (video.length % 3600) % 60
			
			if (h): embed.set_footer(text=f"{h}:{m}:{s}")
			else: embed.set_footer(text=f"{m}:{s}")

		embed.colour = discord.Colour(PAMELLO_C)
		embed.set_thumbnail(url=song.getImageURL())
		for name in os.listdir("../music/youtube"):
			if name == astream.default_filename:
				embed.title = "Song added to queue"
				embed.description = song.getHyperlink()
				await interaction.edit_original_response(embed=embed)
				break
		else:
			embed.description = "Downloading audio..."
			await interaction.edit_original_response(embed=embed)

			
			astream.download("../music/youtube/")

			embed.title = "Song downloaded and added to queue"
			embed.description = song.getHyperlink()
			await interaction.edit_original_response(embed=embed)
		
		player.queueAdd(song)
		player.playnext()
	else:
		await interaction.response.send_message(embed=EEmbed("Only youtube links supported"), ephemeral=True)

@tree.command(name="playlist", description="Add songs from playlist in end of queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	name = "Playlist name"
)
async def playlist(interaction: discord.Interaction, name: str):
	player = findPlayer(interaction)
	if not player:
		if interaction.user.voice:
			players.append(Player(await interaction.user.voice.channel.connect()))
			player = players[-1]
		else:
			await interaction.response.send_message(embed=EEmbed("You must be in voice channel to use this command"), ephemeral=True)
			return
	
	if name != "all":
		for fname in os.listdir("playlists"):
			if fname == (name):
				if player.loadQueue(name, interaction.user):
					await interaction.response.send_message(embed=IEmbed("Songs from playlist \"**{}**\" added to queue".format(ecranate(name))))
				else:
					await interaction.response.send_message(embed=EEmbed("Can`t play this playlist((("), ephemeral=True)
				player.playnext()
				break
		else:
			await interaction.response.send_message(embed=EEmbed("Playlist named \"{}\" not found".format(name)), ephemeral=True)
	else:
		count = player.loadQueue("all", interaction.user)
		if count:
			await interaction.response.send_message(embed=IEmbed("**{}** songs from all playlists added to queue".format(count)))
		else:
			await interaction.response.send_message(embed=EEmbed("Can`t find any playlists((("), ephemeral=True)
		player.playnext()



@tree.command(name="playlists", description="List all playlists", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def playlists(interaction: discord.Interaction):
	string = str()
	for fname in os.listdir("playlists"):
		string += str(fname) + "\n"
	
	embed = IEmbed(string)
	embed.title = "Playlists"

	await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="playepisode", description="Play episode from current song", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	eid = "Episode ID in song (see in queue)"
)
async def playepisode(interaction: discord.Interaction, eid: int):
	player = findPlayer(interaction)
	if player:
		if player.playEpisode(eid - 1):
			song = player.queue[player.nq]
			if len(song.episodes):
				await interaction.response.send_message(embed=IEmbed(f"Song {song.getHyperlink()} rewinded to episode **{song.episodes[eid - 1]['name']}** ([{song.episodes[eid - 1]['timestamp']}]({song.getETimeURL(eid - 1)}))"))
			elif not eid:
				player.jump(player.nq)
				await interaction.response.send_message(embed=IEmbed("Rewinded to song start"))
			else:
				await interaction.response.send_message(embed=EEmbed("Invalid episode ID"), ephemeral=True)
		else:
			await interaction.response.send_message(embed=EEmbed("Invalid episode ID"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="playing", description="Write playing song name", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def playing(interaction: discord.Interaction):
	player = findPlayer(interaction)
	if player:
		song = player.queue[player.nq]
		await interaction.response.send_message(embed=IEmbed("Now playing `{}` - {}\nadded by **{}**".format(player.nq + 1, song.getHyperlink(), song.user.name)), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="jump", description="Jump to song in queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	qid = "Song pos in queue"
)
async def jump(interaction: discord.Interaction, qid: int):
	player = findPlayer(interaction)
	if player:
		if len(player.queue):
			await interaction.response.send_message(embed=IEmbed(f"Jumped to {player.jump(qid - 1).getHyperlink()}"))
		else:
			await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="leap", description="Jump to song in queue and after, return to current song", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	qid = "Song pos in queue"
)
async def leap(interaction: discord.Interaction, qid: int):
	player = findPlayer(interaction)
	if player:
		if len(player.queue):
			await interaction.response.send_message(embed=IEmbed(f"Leaped to {player.leap(qid - 1).getHyperlink()}"))
		else:
			await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="skip", description="Skip current song", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def skip(interaction: discord.Interaction):
	player = findPlayer(interaction)
	if player:
		if len(player.queue):
			await interaction.response.send_message(embed=IEmbed(f"Song {player.skip().getHyperlink()} skipped"))
		else:
			await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="remove", description="Remove song by position in queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	qid = "Song pos in queue"
)
async def remove(interaction: discord.Interaction, qid: int):
	player = findPlayer(interaction)
	if player:
		if len(player.queue):
			await interaction.response.send_message(embed=IEmbed(f"Song {player.remove(qid - 1).getHyperlink()} removed"))
		else:
			await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="removerange", description="Remove songs by from position A to position B in queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	a = "Pos A in queue",
	b = "Pos B in queue"
)
async def removerange(interaction: discord.Interaction, a: int, b: int):
	player = findPlayer(interaction)
	if player:
		if player.removerange(a - 1, b - 1):
			if b > a: a, b = b, a
			await interaction.response.send_message(embed=IEmbed(f"Removed `{a - b + 1}` songs"))
		else:
			await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="swap", description="Swap two songs in queue between themselves", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	a = "Pos A in queue",
	b = "Pos B in queue"
)
async def swap(interaction: discord.Interaction, a: int, b: int):
	player = findPlayer(interaction)
	if player:
		if player.swap(a - 1, b - 1):
			await interaction.response.send_message(embed=IEmbed(f"Songs in pos `{a}` and `{b}` swaped"))
		else:
			await interaction.response.send_message(embed=EEmbed("Invalid position values"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="move", description="Move song in queue to position", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	a = "Pos A in queue",
	b = "Pos B in queue"
)
async def move(interaction: discord.Interaction, a: int, b: int):
	player = findPlayer(interaction)
	if player:
		if player.move(a - 1, b - 1):
			await interaction.response.send_message(embed=IEmbed(f"Song from pos `{a}` moved to pos `{b}`"))
		else:
			await interaction.response.send_message(embed=EEmbed("Invalid position values"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="queue", description="Write queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def queue(interaction: discord.Interaction):
	player = findPlayer(interaction)
	if player:
		message = "" if len(player.queue) else "Empty"
		for i in range(len(player.queue)):
			if (len(message) + len(player.queue[i].getURL()) + len(player.queue[i].user.name) + 22) > 3900:
				message += "   **...**" + str(i) + "/" + str(len(player.queue))
				break
			
			message += "`{}` - {}{}\n".format(
				i + 1,
				"" if not (player.nq == i) else ("**now** > " if player.loopMode != 1 else "**now** single > "),
				player.queue[i].getHyperlink()
			)

			for j in range(len(player.queue[i].episodes)):
				message += f"- - - - `{j + 1}` : [{player.queue[i].episodes[j]['name']}]({player.queue[i].getETimeURL(j)})\n"

			message += "added by **{}**\n".format(ecranate(player.queue[i].user.name))
		
		embed = discord.Embed()
		if player.loopMode == 1: embed.colour = discord.Colour(LOOP1_C)
		elif player.loopMode == 2: embed.colour = discord.Colour(LOOP2_C)
		embed.title = ["Queue", "Queue (single looped)", "Queue (looped)"][player.loopMode]
		embed.description = message
		if len(player.queue): embed.set_image(url=player.queue[player.nq].getImageURL())

		await interaction.response.send_message(embed=embed, ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="shuffle", description="Shuffle queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def shuffle(interaction: discord.Interaction):
	player = findPlayer(interaction)
	if player:
		csong = player.queue[player.nq]
		random.shuffle(player.queue)
		player.nq = player.queue.index(csong)
		if not player.loopMode and player.nq:
			player.queue.insert(0, player.queue.pop(player.nq))
			player.nq = 0

		if len(player.queue): await interaction.response.send_message(embed=IEmbed("Queue shuffled"))
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="loop", description="Loop queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	single = "Loop in single song"
)
async def loop(interaction: discord.Interaction, single: bool = False):
	player = findPlayer(interaction)
	if player:
		if not player.loopMode or (single + 1 == player.loopMode):
			player.loopMode = (not single) + 1
			await interaction.response.send_message(embed=IEmbed("Curent song looped" if single else "Queue is looped"))
		else:
			player.unloop()
			await interaction.response.send_message(embed=IEmbed("Queue is unlooped"))
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="clear", description="Clear queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def clear(interaction: discord.Interaction):
	player = findPlayer(interaction)
	if player:
		if len(player.queue):
			player.clear()
			await interaction.response.send_message(embed=IEmbed("Queue is cleared"))
		else: await interaction.response.send_message(embed=EEmbed("Queue is already empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="mult", description="Mult song in queue", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	qid = "Song pos in queue",
	mult = "Multiplicator"
)
async def mult(interaction: discord.Interaction, qid: int, mult: int):
	player = findPlayer(interaction)
	if player:
		if player.multSong(qid - 1, mult):
			await interaction.response.send_message(embed=IEmbed(f"Song in pos `{qid}` multiplied `{mult}` times"))
		else:
			await interaction.response.send_message(embed=EEmbed(f"Ivalid song position"))
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="pause", description="Pause player", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def pause(interaction: discord.Interaction):
	player = findPlayer(interaction)
	if player:
		await interaction.response.send_message(embed=IEmbed("Player paused" if not player.vclient.is_paused() else "Player already paused"), ephemeral=player.vclient.is_paused())
		player.vclient.pause()
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="resume", description="Resume player", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def resume(interaction: discord.Interaction):
	player = findPlayer(interaction)
	if player:
		await interaction.response.send_message(embed=IEmbed("Player resumed" if player.vclient.is_paused() else "Player already playing"), ephemeral=not player.vclient.is_paused())
		player.vclient.resume()
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="save", description="Save songs from queue to playlist", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
@app_commands.describe(
	name = "Name of playlist",
	overwrite = "If `True` overwrite playlist if it`s already exist"
)
async def save(interaction: discord.Interaction, name: str, overwrite: bool = False):
	player = findPlayer(interaction)
	if player:
		if player.saveQueue(name, overwrite):
			await interaction.response.send_message(embed=IEmbed(f"Playlist **\"{name}\"** saved"))
		else:
			await interaction.response.send_message(embed=EEmbed(f"Playlist **\"{name}\"** already exists (set `overwrite` argument to **True** to overwrite)"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name="exit", description="Kill player", guilds=[discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)])
async def exit(interaction: discord.Interaction):
	player = findPlayer(interaction)
	if player:
		if len(player.queue):
			player.clear()
		await player.vclient.disconnect()
		players.remove(player)
		await interaction.response.send_message(embed=IEmbed("Player killed :skull:"))
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

mainThread = threading.Thread(target=mainloop)
mainThread.start()

client.run("OTA0MjcyNTk2OTE1MzM1MTc5.G6X-3t.4jDNPYbFjNFuJYZpO237rU1zRr7UYL8jaGu4tE")

print("done")
