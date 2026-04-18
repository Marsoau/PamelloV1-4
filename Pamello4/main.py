import discord, os, random, pytube, threading, time
from discord import app_commands
from pytube import extract

from accomands import CACommands
from player import *
from header import *
from helplist import commands as hcommands

class Client(discord.Client):
	def __init__(self):
		super().__init__(intents=discord.Intents.all())
		self.synced = False
		self.cact = None

		self.players = []
	
	def CACrun(self, cac: CACommands, token: str):
		self.cact = threading.Thread(target=cac.mainloop)
		self.run(token=token)

	async def on_ready(self):
		await self.wait_until_ready()
		if not self.synced:
			await tree.sync(guild=discord.Object(id=MAINGUILD_ID))
			self.synced = True
			self.cact.start()
			print(f"logged in as {self.user}")
	
	def get_player(self, gid: int = None):
		for player in self.players:
			if player.vclient.guild.id == gid:
				return player
		return None
	
	async def create_player(self, vchannel: discord.VoiceChannel):
		self.players.append(Player(await vchannel.connect()))
		return self.players[-1]


class IEmbed(discord.Embed):
	def __init__(self, text):
		super().__init__()
		self.description = text
		self.color = INFOС

class EEmbed(discord.Embed):
	def __init__(self, text):
		super().__init__()
		self.title = "Error"
		self.description = text
		self.color = ERRORС

class VEbmed(discord.Embed):
	def __init__(self):
		super().__init__()
		self.title = "Processing..."
		self.description = "Getting audio info..."
	
	async def send(self, interaction: discord.Interaction):
		await interaction.response.send_message(embed=self)

	async def edit(self, interaction: discord.Interaction):
		await interaction.edit_original_response(embed=self)

	def downloading(self):
		self.description = "Downloading audio info..."

	def done(self, new: bool, time: str, song: Song):
		self.color = PAMELLOС
		self.title = f"Song {'downloaded and ' if new else ''}added to queue"
		self.description = song.gethyperlink()
		self.set_footer(text=f"{time} {len(song.episodes) if song.episodes else ''}")
		self.set_thumbnail(url=song.getimageurl())

client = Client()
cacommands = CACommands(client)
tree = app_commands.CommandTree(client)

client.status = discord.Status.dnd

@tree.command(name=hcommands["ping"].name, description=hcommands["ping"].description, guilds=hcommands["ping"].guilds)
async def ping(interaction: discord.Interaction):
	await interaction.response.send_message(embed=IEmbed("pong!"), ephemeral=True)

@tree.command(name=hcommands["play"].name, description=hcommands["play"].description, guilds=hcommands["play"].guilds)
async def play(interaction: discord.Interaction, url: str, inspos: int = 0):
	player = client.get_player(interaction.guild_id)
	if not player:
		if interaction.user.voice:
			player = await client.create_player(interaction.user.voice.channel)
		else:
			await interaction.response.send_message(embed=EEmbed("You must be in voice channel to use this command"), ephemeral=True)
			return
	
	
	if url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be":
		embed = VEbmed()
		await embed.send(interaction)

		video = FYouTube(url)
		song = Song(video.fast_audio.default_filename[:-4], interaction.user, video.video_id)

		if findsong(video.fast_audio.default_filename):
			embed.done(False, video.strtime(), song)
			await embed.edit(interaction)
		else:
			embed.downloading()
			await embed.edit(interaction)

			video.fast_audio.download(MUSICPATH)

			embed.done(True, video.strtime(), song)
			await embed.edit(interaction)
		
		player.queueinsert(song, inspos - 1)
		player.playnext()
	else:
		await interaction.response.send_message(embed=EEmbed("Only youtube links supported"), ephemeral=True)


@tree.command(name=hcommands["playnow"].name, description=hcommands["playnow"].description, guilds=hcommands["playnow"].guilds)
async def playnow(interaction: discord.Interaction, url: str):
	player = client.get_player(interaction.guild_id)
	if not player:
		if interaction.user.voice:
			player = await client.create_player(interaction.user.voice.channel)
		else:
			await interaction.response.send_message(embed=EEmbed("You must be in voice channel to use this command"), ephemeral=True)
			return
	
	
	if url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be":
		embed = VEbmed()
		await embed.send(interaction)

		video = FYouTube(url)
		song = Song(video.fast_audio.default_filename[:-4], interaction.user, video.video_id)

		if findsong(video.fast_audio.default_filename):
			embed.done(False, video.strtime(), song)
			await embed.edit(interaction)
		else:
			embed.downloading()
			await embed.edit(interaction)

			video.fast_audio.download(MUSICPATH)

			embed.done(True, video.strtime(), song)
			await embed.edit(interaction)
		
		if player.queue:
			player.queueinsert(song, player.qn + 1)
			player.skip()
		else:
			player.queueinsert(song)
			player.playnext()
	else:
		await interaction.response.send_message(embed=EEmbed("Only youtube links supported"), ephemeral=True)


@tree.command(name=hcommands["playnext"].name, description=hcommands["playnext"].description, guilds=hcommands["playnext"].guilds)
async def playnext(interaction: discord.Interaction, url: str):
	player = client.get_player(interaction.guild_id)
	if not player:
		if interaction.user.voice:
			player = await client.create_player(interaction.user.voice.channel)
		else:
			await interaction.response.send_message(embed=EEmbed("You must be in voice channel to use this command"), ephemeral=True)
			return
	
	
	if url[:23] == "https://www.youtube.com" or url[:16] == "https://youtu.be":
		embed = VEbmed()
		await embed.send(interaction)

		video = FYouTube(url)
		song = Song(video.fast_audio.default_filename[:-4], interaction.user, video.video_id)

		if findsong(video.fast_audio.default_filename):
			embed.done(False, video.strtime(), song)
			await embed.edit(interaction)
		else:
			embed.downloading()
			await embed.edit(interaction)

			video.fast_audio.download(MUSICPATH)

			embed.done(True, video.strtime(), song)
			await embed.edit(interaction)
		
		if player.queue: player.queueinsert(song, player.qn + 1)
		else: player.queueinsert(song)
		player.playnext()
	else:
		await interaction.response.send_message(embed=EEmbed("Only youtube links supported"), ephemeral=True)


@tree.command(name=hcommands["playlist"].name, description=hcommands["playlist"].description, guilds=hcommands["playlist"].guilds)
async def playlist(interaction: discord.Interaction, name: str, update: bool = False):
	player = client.get_player(interaction.guild_id)
	if not player:
		if interaction.user.voice:
			player = await client.create_player(interaction.user.voice.channel)
		else:
			await interaction.response.send_message(embed=EEmbed("You must be in voice channel to use this command"), ephemeral=True)
			return
	
	count = player.loadqueue(name, interaction.user, update)
	if name != "all":
		if count == -1:
			await interaction.response.send_message(embed=EEmbed(f"Playlist named \"**{ecranate(name)}**\" not found"), ephemeral=True)
		elif count == -2:
			await interaction.response.send_message(embed=EEmbed("Playlist version is uncompatible"), ephemeral=True)
		elif count == -3:
			await interaction.response.send_message(embed=EEmbed("Can`t try to update private playlist"), ephemeral=True)
		else:
			await interaction.response.send_message(embed=IEmbed(f"**{count}** songs from playlist \"**{ecranate(name)}**\" added to queue"))
			player.playnext()
	else:
		if count:
			await interaction.response.send_message(embed=IEmbed(f"**{count}** songs from all playlists added to queue"))
		else:
			await interaction.response.send_message(embed=EEmbed("Can`t play any playlists((("), ephemeral=True)
		player.playnext()

@tree.command(name=hcommands["playepisode"].name, description=hcommands["playepisode"].description, guilds=hcommands["playepisode"].guilds)
async def playepisode(interaction: discord.Interaction, eid: str):
	player = client.get_player(interaction.guild_id)
	if player:
		if player.playepisode(eid - 1):
			song = player.queue[player.nq]
			if len(song.episodes):
				await interaction.response.send_message(embed=IEmbed(f"Song {song.gethyperlink()} rewinded to episode **{song.episodes[eid - 1]['name']}** ([{song.episodes[eid - 1]['timestamp']}]({song.geteurl(eid - 1)}))"))
			elif not eid:
				player.jump(player.nq)
				await interaction.response.send_message(embed=IEmbed("Rewinded to song start"))
			else:
				await interaction.response.send_message(embed=EEmbed("Invalid episode ID"), ephemeral=True)
		else:
			await interaction.response.send_message(embed=EEmbed("Invalid episode ID"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["queue"].name, description=hcommands["queue"].description, guilds=hcommands["queue"].guilds)
async def queue(interaction: discord.Interaction):
	player = client.get_player(interaction.guild_id)
	
	if player:
		length = 0
		message = "" if len(player.queue) else "Empty"
		for i in range(len(player.queue)):
			length += len(player.queue[i].gethyperlink()) + 8
			if length > 3900:
				message += "   **...**" + str(i) + "/" + str(len(player.queue))
				break
			
			message += "`{}` - {}{}\n".format(
				i + 1,
				"" if not (player.qn == i) else ("**now** > " if player.loopmode != 1 else "**now** single > "),
				player.queue[i].gethyperlink()
			)

			for j in range(len(player.queue[i].episodes)):
				message += f"- - - - `{j + 1}` : [{player.queue[i].episodes[j]['name']}]({player.queue[i].geteurl(j)})\n"
				length += 20 + len(player.queue[i].episodes[j]['name']) + len(player.queue[i].geteurl(j))
				
				if length > 3900:
					message += "   **...**" + str(i) + "/" + str(len(player.queue))
					break

			message += "added by **{}**\n".format(ecranate(player.queue[i].user.name))
		
		embed = discord.Embed()
		if player.loopmode == 1: embed.colour = discord.Colour(LOOP1C)
		elif player.loopmode == 2: embed.colour = discord.Colour(LOOP2C)
		embed.title = ["**Queue**", "**Queue** (single looped)", "**Queue** (looped)"][player.loopmode]
		embed.description = message
		if len(player.queue): embed.set_image(url=player.queue[player.qn].getimageurl())

		await interaction.response.send_message(embed=embed, ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["loop"].name, description=hcommands["loop"].description, guilds=hcommands["loop"].guilds)
async def loop(interaction: discord.Interaction, single: bool = False):
	player = client.get_player(interaction.guild_id)
	if player:
		if single:
			if player.loop(1):
				await interaction.response.send_message(embed=IEmbed("Current song looped"))
			else:
				player.loop(2)
				await interaction.response.send_message(embed=IEmbed("Queue looped"), ephemeral=True)
		elif not player.loopmode:
			player.loop(2)
			await interaction.response.send_message(embed=IEmbed("Queue looped"))
		else:
			player.loop(0)
			await interaction.response.send_message(embed=IEmbed("Queue unlooped"))
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["clear"].name, description=hcommands["clear"].description, guilds=hcommands["clear"].guilds)
async def clear(interaction: discord.Interaction):
	player = client.get_player(interaction.guild_id)
	if player:
		player.clear()

		if len(player.queue): await interaction.response.send_message(embed=IEmbed("Queue cleared"))
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["shuffle"].name, description=hcommands["shuffle"].description, guilds=hcommands["shuffle"].guilds)
async def shuffle(interaction: discord.Interaction):
	player = client.get_player(interaction.guild_id)
	if player:
		player.shuffle()

		if len(player.queue): await interaction.response.send_message(embed=IEmbed("Queue shuffled"))
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["move"].name, description=hcommands["move"].description, guilds=hcommands["move"].guilds)
async def move(interaction: discord.Interaction, qid1: int, qid2: int):
	player = client.get_player(interaction.guild_id)
	if player:
		if len(player.queue):
			if player.move(qid1 - 1, qid2 - 1): await interaction.response.send_message(embed=IEmbed(f"Song fron pos `{qid1}` moved to pos `{qid2}`"))
			else: await interaction.response.send_message(embed=EEmbed("Position incorrect"), ephemeral=True)
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["swap"].name, description=hcommands["swap"].description, guilds=hcommands["swap"].guilds)
async def swap(interaction: discord.Interaction, qid1: int, qid2: int):
	player = client.get_player(interaction.guild_id)
	if player:
		if len(player.queue):
			if player.swap(qid1 - 1, qid2 - 1): await interaction.response.send_message(embed=IEmbed(f"Songs in pos `{qid1}` and pos `{qid2}` swaped"))
			else: await interaction.response.send_message(embed=EEmbed("Position incorrect"), ephemeral=True)
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["remove"].name, description=hcommands["remove"].description, guilds=hcommands["remove"].guilds)
async def remove(interaction: discord.Interaction, qid: int):
	player = client.get_player(interaction.guild_id)
	if player:
		if len(player.queue):
			song = player.queue[qid - 1]

			if player.remove(qid - 1): await interaction.response.send_message(embed=IEmbed(f"Song `{qid}` - {song.gethyperlink()} removed"))
			else: await interaction.response.send_message(embed=EEmbed("Position incorrect"), ephemeral=True)
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["removerange"].name, description=hcommands["removerange"].description, guilds=hcommands["removerange"].guilds)
async def removerange(interaction: discord.Interaction, qid1: int, qid2: int):
	player = client.get_player(interaction.guild_id)
	if player:
		if len(player.queue):
			if player.removerange(qid1 - 1, qid2 - 1): await interaction.response.send_message(embed=IEmbed(f"Songs from pos `{qid1}` to pos `{qid2}` removed"))
		else: await interaction.response.send_message(embed=EEmbed("Positions incorrect"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["skip"].name, description=hcommands["skip"].description, guilds=hcommands["skip"].guilds)
async def skip(interaction: discord.Interaction):
	player = client.get_player(interaction.guild_id)
	if player:
		if len(player.queue):
			song = player.queue[player.qn]

			player.skip()
			await interaction.response.send_message(embed=IEmbed(f"Song {song.gethyperlink()} skiped"))
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["jump"].name, description=hcommands["jump"].description, guilds=hcommands["jump"].guilds)
async def jump(interaction: discord.Interaction, qid: int):
	player = client.get_player(interaction.guild_id)
	if player:
		if len(player.queue):
			song = player.queue[qid - 1]

			if player.jump(qid - 1): await interaction.response.send_message(embed=IEmbed(f"Jumpeed to `{qid}` - {song.gethyperlink()}"))
			else: await interaction.response.send_message(embed=EEmbed("Position incorrect"), ephemeral=True)
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["step"].name, description=hcommands["step"].description, guilds=hcommands["step"].guilds)
async def step(interaction: discord.Interaction, qid: int):
	player = client.get_player(interaction.guild_id)
	if player:
		if len(player.queue):
			song = player.queue[qid - 1]

			if player.step(qid - 1): await interaction.response.send_message(embed=IEmbed(f"Stepped on `{qid}` - {song.gethyperlink()}"))
			else: await interaction.response.send_message(embed=EEmbed("Position incorrect"), ephemeral=True)
		else: await interaction.response.send_message(embed=IEmbed("Queue is empty"), ephemeral=True)
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["savelist"].name, description=hcommands["savelist"].description, guilds=hcommands["savelist"].guilds)
async def savelist(interaction: discord.Interaction, name: str, overwrite: bool = False, private: bool = False):
	player = client.get_player(interaction.guild_id)
	if not player:
		if interaction.user.voice:
			player = await client.create_player(interaction.user.voice.channel)
		else:
			await interaction.response.send_message(embed=EEmbed("You must be in voice channel to use this command"), ephemeral=True)
			return
	
	code = player.savequeue(name, overwrite, private, interaction.user.id)
	if name != "all":
		if code == -1:
			await interaction.response.send_message(embed=EEmbed("Can`t overwrite playlist").set_footer(text="use `overwrite` parameter to overwrite existing playlists"), ephemeral=True)
		elif code == -2:
			await interaction.response.send_message(embed=EEmbed("Playlist version is uncompatible for owerwriting"), ephemeral=True)
		elif code == -3:
			await interaction.response.send_message(embed=EEmbed("Can`t overwrite private playlist"), ephemeral=True)
		else:
			await interaction.response.send_message(embed=IEmbed(f"Songs from queue saved in playlist named \"**{ecranate(name)}**\""))
			player.playnext()
	else:
		await interaction.response.send_message(embed=EEmbed("Can`t save playlist named **all**"), ephemeral=True)
		player.playnext()

@tree.command(name=hcommands["pause"].name, description=hcommands["pause"].description, guilds=hcommands["pause"].guilds)
async def pause(interaction: discord.Interaction):
	player = client.get_player(interaction.guild_id)
	if player:
		await interaction.response.send_message(embed=IEmbed("Player paused" if not player.vclient.is_paused() else "Player already paused"), ephemeral=player.vclient.is_paused())
		player.vclient.pause()
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["resume"].name, description=hcommands["resume"].description, guilds=hcommands["resume"].guilds)
async def resume(interaction: discord.Interaction):
	player = client.get_player(interaction.guild_id)
	if player:
		await interaction.response.send_message(embed=IEmbed("Player resumed" if player.vclient.is_paused() else "Player already playing"), ephemeral=not player.vclient.is_paused())
		player.vclient.resume()
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

@tree.command(name=hcommands["exit"].name, description=hcommands["exit"].description, guilds=hcommands["exit"].guilds)
async def exit(interaction: discord.Interaction):
	player = client.get_player(interaction.guild_id)
	if player:
		await player.vclient.disconnect()
		client.players.remove(player)
		
		await interaction.response.send_message(embed=IEmbed("Player killed"))
	else: await interaction.response.send_message(embed=EEmbed("Can`t find players in this guild"), ephemeral=True)

client.CACrun(cacommands, TOKEN)
