import discord, pytube, os
from discord import app_commands

RESET = '\033[0m'

MAINSERV_ID = 878040480179433482
TESTGUILD_ID = 1032966863661043813
MY_ID = 544933092503060509

audioPlayers = []
excepted_roles = [904273914077778001]

def ecranate(text: str):
	text = text.replace("_", "\_")
	text = text.replace("`", "\`")
	text = text.replace("~", "\~")
	text = text.replace("*", "\*")
	text = text.replace("|", "\|")
	return text

def color(red, green, blue):
	return f'\033[38;2;{red};{green};{blue}m'



class AClient(discord.Client):
	def __init__(self):
		super().__init__(intents=discord.Intents.default())
		self.synced = False

	async def on_ready(self):
		await self.wait_until_ready()
		if not self.synced:
			await tree.sync(guild=discord.Object(id=MAINSERV_ID))
			self.synced = True
			print(f"logged in as {self.user}")


class AudioPlayer(object):
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



client = AClient()
tree = app_commands.CommandTree(client)


@tree.command(name="ping", description="ping-pong")
async def ping(interaction: discord.Interaction):
	await interaction.response.send_message("pong")


@tree.command(name="test", description="none", guild=discord.Object(id=MAINSERV_ID))
async def test(interaction: discord.Interaction):
	guild = interaction.guild
	everyone = guild.roles[0]

	for role in guild.roles:
		print("\n", color(role.colour.r, role.colour.g, role.colour.b) + role.name, RESET, end="", sep="")

		if (role.permissions != guild.roles[0].permissions):
			print()

			if role.permissions.add_reactions != everyone.permissions.add_reactions:
				print("\tadd_reactions: ", color(0, 255, 0) if role.permissions.add_reactions else color(255, 0, 0), role.permissions.add_reactions, RESET, sep="")
			if role.permissions.administrator != everyone.permissions.administrator:
				print("\tadministrator: ", color(0, 255, 0) if role.permissions.administrator else color(255, 0, 0), role.permissions.administrator, RESET, sep="")
			if role.permissions.attach_files != everyone.permissions.attach_files:
				print("\tattach_files: ", color(0, 255, 0) if role.permissions.attach_files else color(255, 0, 0), role.permissions.attach_files, RESET, sep="")
			if role.permissions.ban_members != everyone.permissions.ban_members:
				print("\tban_members: ", color(0, 255, 0) if role.permissions.ban_members else color(255, 0, 0), role.permissions.ban_members, RESET, sep="")
			if role.permissions.change_nickname != everyone.permissions.change_nickname:
				print("\tchange_nickname: ", color(0, 255, 0) if role.permissions.change_nickname else color(255, 0, 0), role.permissions.change_nickname, RESET, sep="")
			if role.permissions.connect != everyone.permissions.connect:
				print("\tconnect: ", color(0, 255, 0) if role.permissions.connect else color(255, 0, 0), role.permissions.connect, RESET, sep="")
			if role.permissions.create_instant_invite != everyone.permissions.create_instant_invite:
				print("\tcreate_instant_invite: ", color(0, 255, 0) if role.permissions.create_instant_invite else color(255, 0, 0), role.permissions.create_instant_invite, RESET, sep="")
			if role.permissions.create_private_threads != everyone.permissions.create_private_threads:
				print("\tcreate_private_threads: ", color(0, 255, 0) if role.permissions.create_private_threads else color(255, 0, 0), role.permissions.create_private_threads, RESET, sep="")
			if role.permissions.create_public_threads != everyone.permissions.create_public_threads:
				print("\tcreate_public_threads: ", color(0, 255, 0) if role.permissions.create_public_threads else color(255, 0, 0), role.permissions.create_public_threads, RESET, sep="")
			if role.permissions.deafen_members != everyone.permissions.deafen_members:
				print("\tdeafen_members: ", color(0, 255, 0) if role.permissions.deafen_members else color(255, 0, 0), role.permissions.deafen_members, RESET, sep="")
			if role.permissions.embed_links != everyone.permissions.embed_links:
				print("\tembed_links: ", color(0, 255, 0) if role.permissions.embed_links else color(255, 0, 0), role.permissions.embed_links, RESET, sep="")
			if role.permissions.external_emojis != everyone.permissions.external_emojis:
				print("\texternal_emojis: ", color(0, 255, 0) if role.permissions.external_emojis else color(255, 0, 0), role.permissions.external_emojis, RESET, sep="")
			if role.permissions.external_stickers != everyone.permissions.external_stickers:
				print("\texternal_stickers: ", color(0, 255, 0) if role.permissions.external_stickers else color(255, 0, 0), role.permissions.external_stickers, RESET, sep="")
			if role.permissions.kick_members != everyone.permissions.kick_members:
				print("\tkick_members: ", color(0, 255, 0) if role.permissions.kick_members else color(255, 0, 0), role.permissions.kick_members, RESET, sep="")
			if role.permissions.manage_channels != everyone.permissions.manage_channels:
				print("\tmanage_channels: ", color(0, 255, 0) if role.permissions.manage_channels else color(255, 0, 0), role.permissions.manage_channels, RESET, sep="")
			if role.permissions.manage_emojis != everyone.permissions.manage_emojis:
				print("\tmanage_emojis: ", color(0, 255, 0) if role.permissions.manage_emojis else color(255, 0, 0), role.permissions.manage_emojis, RESET, sep="")
			if role.permissions.manage_emojis_and_stickers != everyone.permissions.manage_emojis_and_stickers:
				print("\tmanage_emojis_and_stickers: ", color(0, 255, 0) if role.permissions.manage_emojis_and_stickers else color(255, 0, 0), role.permissions.manage_emojis_and_stickers, RESET, sep="")
			if role.permissions.manage_events != everyone.permissions.manage_events:
				print("\tmanage_events: ", color(0, 255, 0) if role.permissions.manage_events else color(255, 0, 0), role.permissions.manage_events, RESET, sep="")
			if role.permissions.manage_guild != everyone.permissions.manage_guild:
				print("\tmanage_guild: ", color(0, 255, 0) if role.permissions.manage_guild else color(255, 0, 0), role.permissions.manage_guild, RESET, sep="")
			if role.permissions.manage_messages != everyone.permissions.manage_messages:
				print("\tmanage_messages: ", color(0, 255, 0) if role.permissions.manage_messages else color(255, 0, 0), role.permissions.manage_messages, RESET, sep="")
			if role.permissions.manage_nicknames != everyone.permissions.manage_nicknames:
				print("\tmanage_nicknames: ", color(0, 255, 0) if role.permissions.manage_nicknames else color(255, 0, 0), role.permissions.manage_nicknames, RESET, sep="")
			if role.permissions.manage_permissions != everyone.permissions.manage_permissions:
				print("\tmanage_permissions: ", color(0, 255, 0) if role.permissions.manage_permissions else color(255, 0, 0), role.permissions.manage_permissions, RESET, sep="")
			if role.permissions.manage_roles != everyone.permissions.manage_roles:
				print("\tmanage_roles: ", color(0, 255, 0) if role.permissions.manage_roles else color(255, 0, 0), role.permissions.manage_roles, RESET, sep="")
			if role.permissions.manage_threads != everyone.permissions.manage_threads:
				print("\tmanage_threads: ", color(0, 255, 0) if role.permissions.manage_threads else color(255, 0, 0), role.permissions.manage_threads, RESET, sep="")
			if role.permissions.manage_webhooks != everyone.permissions.manage_webhooks:
				print("\tmanage_webhooks: ", color(0, 255, 0) if role.permissions.manage_webhooks else color(255, 0, 0), role.permissions.manage_webhooks, RESET, sep="")
			if role.permissions.mention_everyone != everyone.permissions.mention_everyone:
				print("\tmention_everyone: ", color(0, 255, 0) if role.permissions.mention_everyone else color(255, 0, 0), role.permissions.mention_everyone, RESET, sep="")
			if role.permissions.moderate_members != everyone.permissions.moderate_members:
				print("\tmoderate_members: ", color(0, 255, 0) if role.permissions.moderate_members else color(255, 0, 0), role.permissions.moderate_members, RESET, sep="")
			if role.permissions.move_members != everyone.permissions.move_members:
				print("\tmove_members: ", color(0, 255, 0) if role.permissions.move_members else color(255, 0, 0), role.permissions.move_members, RESET, sep="")
			if role.permissions.mute_members != everyone.permissions.mute_members:
				print("\tmute_members: ", color(0, 255, 0) if role.permissions.mute_members else color(255, 0, 0), role.permissions.mute_members, RESET, sep="")
			if role.permissions.priority_speaker != everyone.permissions.priority_speaker:
				print("\tpriority_speaker: ", color(0, 255, 0) if role.permissions.priority_speaker else color(255, 0, 0), role.permissions.priority_speaker, RESET, sep="")
			if role.permissions.read_message_history != everyone.permissions.read_message_history:
				print("\tread_message_history: ", color(0, 255, 0) if role.permissions.read_message_history else color(255, 0, 0), role.permissions.read_message_history, RESET, sep="")
			if role.permissions.read_messages != everyone.permissions.read_messages:
				print("\tread_messages: ", color(0, 255, 0) if role.permissions.read_messages else color(255, 0, 0), role.permissions.read_messages, RESET, sep="")
			if role.permissions.request_to_speak != everyone.permissions.request_to_speak:
				print("\trequest_to_speak: ", color(0, 255, 0) if role.permissions.request_to_speak else color(255, 0, 0), role.permissions.request_to_speak, RESET, sep="")
			if role.permissions.send_messages != everyone.permissions.send_messages:
				print("\tsend_messages: ", color(0, 255, 0) if role.permissions.send_messages else color(255, 0, 0), role.permissions.send_messages, RESET, sep="")
			if role.permissions.send_messages_in_threads != everyone.permissions.send_messages_in_threads:
				print("\tsend_messages_in_threads: ", color(0, 255, 0) if role.permissions.send_messages_in_threads else color(255, 0, 0), role.permissions.send_messages_in_threads, RESET, sep="")
			if role.permissions.send_tts_messages != everyone.permissions.send_tts_messages:
				print("\tsend_tts_messages: ", color(0, 255, 0) if role.permissions.send_tts_messages else color(255, 0, 0), role.permissions.send_tts_messages, RESET, sep="")
			if role.permissions.speak != everyone.permissions.speak:
				print("\tspeak: ", color(0, 255, 0) if role.permissions.speak else color(255, 0, 0), role.permissions.speak, RESET, sep="")
			if role.permissions.stream != everyone.permissions.stream:
				print("\tstream: ", color(0, 255, 0) if role.permissions.stream else color(255, 0, 0), role.permissions.stream, RESET, sep="")
			if role.permissions.use_application_commands != everyone.permissions.use_application_commands:
				print("\tuse_application_commands: ", color(0, 255, 0) if role.permissions.use_application_commands else color(255, 0, 0), role.permissions.use_application_commands, RESET, sep="")
			if role.permissions.use_embedded_activities != everyone.permissions.use_embedded_activities:
				print("\tuse_embedded_activities: ", color(0, 255, 0) if role.permissions.use_embedded_activities else color(255, 0, 0), role.permissions.use_embedded_activities, RESET, sep="")
			if role.permissions.use_external_emojis != everyone.permissions.use_external_emojis:
				print("\tuse_external_emojis: ", color(0, 255, 0) if role.permissions.use_external_emojis else color(255, 0, 0), role.permissions.use_external_emojis, RESET, sep="")
			if role.permissions.use_external_stickers != everyone.permissions.use_external_stickers:
				print("\tuse_external_stickers: ", color(0, 255, 0) if role.permissions.use_external_stickers else color(255, 0, 0), role.permissions.use_external_stickers, RESET, sep="")
			if role.permissions.use_voice_activation != everyone.permissions.use_voice_activation:
				print("\tuse_voice_activation: ", color(0, 255, 0) if role.permissions.use_voice_activation else color(255, 0, 0), role.permissions.use_voice_activation, RESET, sep="")
			if role.permissions.value != everyone.permissions.value:
				print("\tvalue: ", color(0, 255, 0) if role.permissions.value else color(255, 0, 0), role.permissions.value, RESET, sep="")
			if role.permissions.view_audit_log != everyone.permissions.view_audit_log:
				print("\tview_audit_log: ", color(0, 255, 0) if role.permissions.view_audit_log else color(255, 0, 0), role.permissions.view_audit_log, RESET, sep="")
			if role.permissions.view_channel != everyone.permissions.view_channel:
				print("\tview_channel: ", color(0, 255, 0) if role.permissions.view_channel else color(255, 0, 0), role.permissions.view_channel, RESET, sep="")
			if role.permissions.view_guild_insights != everyone.permissions.view_guild_insights:
				print("\tview_guild_insights: ", color(0, 255, 0) if role.permissions.view_guild_insights else color(255, 0, 0), role.permissions.view_guild_insights, RESET, sep="")
			
			print("\n\tUsers: ")
			for member in role.members:
				print("\t", member.name, sep="")
			if not len(role.members): print("\tNone")
		else:
			print(": ", color(0, 255, 0) + "good", RESET, sep="")
		
		
	await interaction.response.send_message(content="Done. check console")



@tree.command(name="listroles", description="List roles with high permisions", guild=discord.Object(id=MAINSERV_ID))
async def listroles(interaction: discord.Interaction):
	guild = interaction.guild
	
	highPermisions = len(guild.roles) - len(excepted_roles)
	for role in guild.roles:
		print("\n", color(role.colour.r, role.colour.g, role.colour.b) + role.name, RESET, end="", sep="")
		
		if (role.permissions.administrator or
			role.permissions.manage_roles or
			role.permissions.manage_guild or
			role.permissions.manage_channels):
			print()

			if role.permissions.administrator:
				print(color(255, 0, 0) + "\tadministrator", RESET, sep="")
			elif role.permissions.manage_roles:
				print(color(255, 0, 0) + "\tmanage_roles", RESET, sep="")
			elif role.permissions.manage_guild:
				print(color(255, 0, 0) + "\tmanage_guild", RESET, sep="")
			elif role.permissions.manage_channels:
				print(color(255, 0, 0) + "\tmanage_channels", RESET, sep="")

			print("\n\tUsers: ")
			for member in role.members:
				print("\t", member.name, sep="")
			if not len(role.members): print("\tNone")
		else:
			highPermisions -= 1
			print(": ", color(0, 255, 0) + "good", RESET, sep="")
	
	await interaction.response.send_message(content=f"Done. {highPermisions} high permisions of {len(guild.roles)} roles." + " check console for more information" if highPermisions else "")

@tree.command(name="reapairroles", description="Removes excessive permissions from a role", guild=discord.Object(id=878040480179433482))
async def reapairroles(interaction: discord.Interaction):
	guild = interaction.guild
	
	changes = 0
	for role in guild.roles:
		if (role.id in excepted_roles): continue

		if (role.permissions.administrator or
			role.permissions.manage_roles or
			role.permissions.manage_guild or
			role.permissions.manage_channels):
			print(color(role.colour.r, role.colour.g, role.colour.b), role.name, RESET)
			changes = changes + 1

			uPermissions = role.permissions
			if uPermissions.administrator:
				uPermissions.administrator = False
				print("\tRemoved administrator permission")
			elif uPermissions.manage_roles:
				uPermissions.manage_roles = False
				print("\tRemoved manage_roles permission")
			elif uPermissions.manage_guild:
				uPermissions.manage_guild = False
				print("\tRemoved manage_guild permission")
			elif uPermissions.manage_channels:
				uPermissions.manage_channels = False
				print("\tRemoved manage_channels permission")

			await role.edit(permissions = uPermissions)


	await interaction.response.send_message(content="Done. " + str(changes) + " roles changed. check console for more information")

@tree.command(name="play", description="Add song to queue end", guild=discord.Object(id=MAINSERV_ID))
async def play(interaction: discord.Interaction, url: str):
	audioPlayer = None
	if len(audioPlayers):
		for i in range(len(audioPlayers)):
			if audioPlayers[i].guildID == interaction.guild.id:
				audioPlayer = audioPlayers[i]
				break

	if audioPlayer is None:
		audioPlayers.append(AudioPlayer(interaction.guild.id, await interaction.user.voice.channel.connect()))
		audioPlayer = audioPlayers[-1]
	
	print(url)
	if url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be":
		await interaction.response.send_message(content="Getting audio info...")

		video = pytube.YouTube(url)
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
			await interaction.edit_original_response(content="**" + first.default_filename + "** added to queue")
		else:
			await interaction.edit_original_response(content="Downloading audio...")

			vidStreams = video.streams.all()
			tStream = None

			for stream in vidStreams:
				if stream.type == "audio" and stream.abr == "128kbps":
					tStream = stream
			
			tStream.download("D:/Discord/UPamello/music")
			await interaction.edit_original_response(content="**" + tStream.default_filename + "** downloaded and added to queue")
		
		audioPlayer.queueAppend(first.default_filename, interaction.user)
	else:
		await interaction.response.send_message(content="Only youtube links suported")
	
	
	audioPlayer.play()


@tree.command(name="loop", description="Loop queue", guild=discord.Object(id=MAINSERV_ID))
async def loop(interaction: discord.Interaction):
	player = None
	if len(audioPlayers) > 0:
		for i in range(len(audioPlayers)):
			if audioPlayers[i].guildID == interaction.guild.id:
				player = audioPlayers[i]
				break
		else:
			await interaction.response.send_message("Can`t find music players in this guild")
			return
	
		await interaction.response.send_message("The queue is looped" if player.loop() else "The queue is no longer looped")

@tree.command(name="queue", description="Show the queue", guild=discord.Object(id=MAINSERV_ID))
async def queue(interaction: discord.Interaction):
	audioPlayer = None
	if len(audioPlayers):
		for i in range(len(audioPlayers)):
			if audioPlayers[i].guildID == interaction.guild.id:
				audioPlayer = audioPlayers[i]
				break
		else:
			await interaction.response.send_message("Can`t find music players in this guild")
			return
	
		if audioPlayer is not None:
			qstr = audioPlayer.getQueueString()

			await interaction.response.send_message(qstr if qstr != "" else "Queue is empty")

@tree.command(name="skip", description="Skip current song", guild=discord.Object(id=MAINSERV_ID))
async def skip(interaction: discord.Interaction):
	audioPlayer = None
	if len(audioPlayers):
		for i in range(len(audioPlayers)):
			if audioPlayers[i].guildID == interaction.guild.id:
				audioPlayer = audioPlayers[i]
				break
		else:
			await interaction.response.send_message("Can`t find music players in this guild")
			return
		
		if len(audioPlayer.queue):
			await interaction.response.send_message("**" + audioPlayer.skip() + "** skiped")
		else:
			await interaction.response.send_message("Queue is empty")

@tree.command(name="clearqueue", description="Clear the queue", guild=discord.Object(id=MAINSERV_ID))
async def clearqueue(interaction: discord.Interaction):
	audioPlayer = None
	if len(audioPlayers):
		for i in range(len(audioPlayers)):
			if audioPlayers[i].guildID == interaction.guild.id:
				audioPlayer = audioPlayers[i]
				break
		else:
			await interaction.response.send_message("Can`t find music players in this guild")
			return
		
		await interaction.response.send_message("Queue cleared" if audioPlayer.clearQueue() else "Queue already empty")

@tree.command(name="showplayers", description="None", guild=discord.Object(id=MAINSERV_ID))
async def showplayers(interaction: discord.Interaction):
	if interaction.user.id == MY_ID:
		if len(audioPlayers) > 0:
			plstr = ""
			for i in range(len(audioPlayers)):
				plstr += f"**{i + 1}.** `{audioPlayers[i].guildID}`\n"
			
			await interaction.response.send_message(plstr)

	else:
		await interaction.response.send_message("You don`t have permission to this command")

@tree.command(name="pause", description="Pause song", guild=discord.Object(id=MAINSERV_ID))
async def pause(interaction: discord.Interaction):
	audioPlayer = None
	if len(audioPlayers):
		for i in range(len(audioPlayers)):
			if audioPlayers[i].guildID == interaction.guild.id:
				audioPlayer = audioPlayers[i]
				break
		else:
			await interaction.response.send_message("Can`t find music players in this guild")
			return
	else:
		await interaction.response.send_message("Can`t find music players")



client.run("OTA0MjcyNTk2OTE1MzM1MTc5.G6X-3t.4jDNPYbFjNFuJYZpO237rU1zRr7UYL8jaGu4tE")

