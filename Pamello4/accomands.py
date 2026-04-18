import discord
from header import MY_ID

ORANGE = 0xFF8462
BLUE = 0x4040FF
GREY = 0x5F5F5F
RED = 0xFF4040
YELLOW = 0xFFD562
RESET = '\033[0m'

def fnum(text: str):
	return f"{ccolor(ORANGE)}{text}{RESET}"
def ftext(text: str):
	return f"{ccolor(GREY)}\"{ccolor(YELLOW)}{text}{ccolor(GREY)}\"{RESET}"

def ccolor(colorcode: int):
	red = colorcode // 65536
	green = (colorcode - red * 65536) // 256
	
	return f'\033[38;2;{red};{green};{colorcode - red * 65536 - green * 256}m'

def clink(url: str, label: str):
    return f'\033]8;;{url}\033\\{label}\033]8;;\033\\'


class CACommands():
	def __init__(self, client: discord.Client):
		self.client = client
		self.player = None
		pass

	def listplayers(self):
		if not len(self.client.players):
			print("Can`t find any players")
		for player in self.client.players:
			print(f"{fnum(player.vclient.guild.id)} : {ftext(player.vclient.guild.name)}")
		
		return len(self.client.players)
	
	def playlist(self, name: str):
		count = self.player.loadqueue(name, self.player.vclient.guild.get_member(MY_ID), False)
		if name != "all":
			if count == -1:
				print(f"Playlist named {ftext(name)} not found")
			elif count == -2:
				print("Playlist version is uncompatible")
			elif count == -3:
				print("Playlist is private")
			else:
				print(f"{fnum(count)} songs from playlist {ftext(name)} added to queue")
				self.player.playnext()
		else:
			if count:
				print(f"{fnum(count)} songs from all playlists added to queue")
			else:
				print("Can`t play any playlists(((")
	
	def mainloop(self):
		try:
			while True:
				c = input().split()

				if c[0] == "setactive":
					if not self.listplayers(): continue
					self.player = self.client.players[int(input("make active > "))]
				
				elif c[0] == "players":
					if not self.player and not self.listplayers(): continue

				elif self.player:
					if c[0] == "playlist":
						self.playlist(c[1])
					
					elif c[0] == "queue":
						for j in range(len(self.player.queue)):
							color = self.player.queue[j].user.color
							print(f"{ccolor(RED)}{'now > ' if j == self.player.qn else ''}{ccolor(GREY)}{j}{RESET} - {ccolor(BLUE)}{clink(self.player.queue[j].geturl(), self.player.queue[j].name)}{RESET}")
							print(f"added by \033[38;2;{color.r};{color.g};{color.b}m" + f"{self.player.queue[j].user.name}{RESET}")
				elif not self.player:
					print(f"You doesn`t have active player, use command {ftext('setactive')}")
		except Exception as ex: print(ex)