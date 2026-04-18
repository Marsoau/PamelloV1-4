import discord, random, pytube, os
from discord.ext import commands

def ecranate(text: str):
	text = text.replace("_", "\_")
	text = text.replace("`", "\`")
	text = text.replace("~", "\~")
	text = text.replace("*", "\*")
	text = text.replace("|", "\|")
	return text


class Player(object):
	def __init__(self, guildID, vClient):
		self.guildID = guildID
		self.vClient = vClient
		self.queueN = 0
		self.queue = []

		self.is_playerActive = False
		self.is_loop = False

	def loop(self):
		self.is_loop = not self.is_loop

		if not self.is_loop:
			for i in range(self.queueN):
				self.queue.remove(self.queue[i])

		return self.is_loop

	def afterSong(self, a):
		self.is_playerActive = False

		if self.is_loop:
			if len(self.queue) > self.queueN + 1:
				self.queueN += 1
			else:
				self.queueN = 0
			self.play()
		else:
			self.queueN = 0

			self.queue.remove(self.queue[0])
			self.play()
	
	def skip(self):
		if len(self.queue):
			if self.queueN > 0:
				self.queueN -= 1
			
			self.vClient.stop()
			return self.queue[self.queueN]["name"]
		return None
	
	def play(self):
		if len(self.queue):
			if not self.is_playerActive:
				self.vClient.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="music/" + self.queue[self.queueN]["name"]), after=self.afterSong)
				self.is_playerActive = True
			elif self.vClient.is_paused():
				self.vClient.resume()
		else:
			self.vClient.stop()
			self.is_playerActive = False


	def queueAppend(self, songname, customer):
		self.queue.append({
			"name": songname,
			"customer": customer
		})
	
	def queueAppendNext(self, songname, customer):
		self.queue.insert(self.queueN + 1, {
			"name": songname,
			"customer": customer
		})
	
	def getQueueString(self):
		qstr = ""
		for song in self.queue:
			qstr += f"**{ecranate(song['name'])}** added by **{ecranate(str(song['customer']))}**\n"
		return qstr


client = commands.Bot(command_prefix="&", intents=discord.Intents.default())
client.remove_command("help")

players = []

@client.event
async def on_ready():
	print(client.user.name + " is here! " + random.choice(["✌️", "👋", "🤘", "🤟"]))


@client.event
async def on_message(message):
	if message.author != client.user:
		print(message.author, ": ", message.content, sep="")
	message.content = message.content.split(" ", 1)[1]
	await client.process_commands(message)

@client.command()
async def testc(ctx, num):
	global test

	test += int(num)
	await ctx.channel.send(str(test))

@client.command()
async def play(ctx, songname):
	player = None
	if len(players):
		for i in range(len(players)):
			if players[i].guildID == ctx.guild.id:
				player = players[i]
				break
	
	if player is None:
		players.append(Player(ctx.guild.id, await ctx.message.author.voice.channel.connect()))
		player = players[-1]
		await ctx.channel.send("Created new player for guild **#" + str(ctx.guild.id) + "**")
	
	if songname[:23] == "https://www.youtube.com":
		await ctx.channel.send("Getting audio info...")
		video = pytube.YouTube(songname)
		first = video.streams.filter(type="audio")
		first = first.first()
		file_exist = False

		for name in os.listdir("music"):
			if first.default_filename == name:
				print(first.default_filename, "==", name)
				file_exist = True
				break
			else:
				print(first.default_filename, "!=", name)
		
		if file_exist:
			await ctx.channel.send("**" + first.default_filename + "** added to queue")
		else:
			await ctx.channel.send("Downloading audio...")

			vidStreams = video.streams.all()
			tStream = None

			for stream in vidStreams:
				if stream.type == "audio" and stream.abr == "128kbps":
					tStream = stream
			
			tStream.download("D:\Discord\Bot\music")
			await ctx.channel.send("**" + tStream.default_filename + "** downloaded and added to queue")
		
		player.queueAppend(first.default_filename, ctx.message.author)
	elif songname[len(songname) - 4:] == ".mp3":
		print("mp3")
		player.queueAppend(songname, ctx.message.author)
		await ctx.channel.send("**" + songname + "** added to queue")
	else:
		print(songname[len(songname) - 4:], "!= .mp3")
		print("el")
	
	
	player.play()

@client.command()
async def loop(ctx):
	player = None
	if len(players) > 0:
		for i in range(len(players)):
			if players[i].guildID == ctx.guild.id:
				player = players[i]
				break
		else:
			await ctx.channel.send("Can`t find music players in this guild")
			return
	
		await ctx.channel.send("The queue is looped" if player.loop() else "The queue is no longer looped")

@client.command()
async def queue(ctx):
	player = None
	if len(players):
		for i in range(len(players)):
			if players[i].guildID == ctx.guild.id:
				player = players[i]
				break
		else:
			await ctx.channel.send("Can`t find music players in this guild")
			return
	
		if player is not None:
			qstr = player.getQueueString()

			await ctx.channel.send(qstr if qstr != "" else "Queue is empty")

@client.command()
async def skip(ctx):
	player = None
	if len(players):
		for i in range(len(players)):
			if players[i].guildID == ctx.guild.id:
				player = players[i]
				break
		else:
			await ctx.channel.send("Can`t find music players in this guild")
			return
		
		if len(player.queue):
			await ctx.channel.send("**" + player.skip() + "** skiped")
		else:
			await ctx.channel.send("Queue is empty")

@client.command()
async def clearqueue(ctx):
	player = None
	if len(players):
		for i in range(len(players)):
			if players[i].guildID == ctx.guild.id:
				player = players[i]
				break
		else:
			await ctx.channel.send("Can`t find music players in this guild")
			return
		
		await ctx.channel.send("Queue cleared" if player.clearQueue() else "Queue already empty")

@client.command()
async def showplayers(ctx, n:int = None):
	if ctx.message.author.id == 544933092503060509:
		if n is None:
			if len(players) > 0:
				plstr = ""
				for i in range(len(players)):
					plstr += f"**{i + 1}.** `{players[i].guildID}`\n"
				
				await ctx.channel.send(plstr)
		elif n <= len(players) and n > 0:
			n -= 1

	else:
		await ctx.channel.send("You don`t have access to this command")


client.run("OTA0MjcyNTk2OTE1MzM1MTc5.G6X-3t.4jDNPYbFjNFuJYZpO237rU1zRr7UYL8jaGu4tE")
