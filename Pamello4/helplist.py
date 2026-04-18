import discord
from header import MAINGUILD_ID, TESTGUILD_ID

class HCommand():
	def __init__(self, name: str, description: str, guilds: list[discord.abc.Snowflake] = [discord.Object(id=MAINGUILD_ID), discord.Object(id=TESTGUILD_ID)]):
		self.name = name
		self.description = description
		self.guilds = guilds

commands = {
	"play": HCommand("play", "add song to end of queue, or, if indicated, to position `qid`"),
	"playnow": HCommand("playnow", "add song at position to now playing song and play immediately"),
	"playnext": HCommand("playnext", "add song to queue at position after current song"),
	"playlist": HCommand("playlist", "add songs from playlist to end of queue"),
	"playepisode": HCommand("playerpisode", "rewind current song to episode `eid`"),
	"playlists": HCommand("playlists", "write all playlists"),
	"plays": HCommand("plays", "write current playing song"),
	
	"queue": HCommand("queue", "write queue"),
	"shuffle": HCommand("shuffle", "shuffle queue"),
	"clear": HCommand("clear", "clear queue"),
	"loop": HCommand("loop", "loop/unloop single song/queue"),
	"move": HCommand("move", "move song from position `qid1` to position `qid2`"),
	"swap": HCommand("swap", "swap songs in positions `qid1` and `qid2` between themselfes"),
	
	"remove": HCommand("remove", "remove song in position `qid` from queue"),
	"removerange": HCommand("removerange", "remove songs from position `qid1` to position `qid2` from queue"),

	"skip": HCommand("skip", "skip current song"),
	"jump": HCommand("jump", "immediately play song in position `qid`"),
	"step": HCommand("step", "play song in position `qid` after curent song"),

	"savelist": HCommand("savelist", "save songs from queue to playlist"),

	"pause": HCommand("pause", "pause current song"),
	"resume": HCommand("resume", "resume current song"),

	"ping": HCommand("ping", "check bot connection"),
	"exit": HCommand("exit", "delete music player on this server"),
}
