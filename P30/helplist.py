commands = {
	"commands": """**Adding song to queue**
> play
> playing
> playlist
> playepisode

**Queue manipulations**
> queue
> jump
> skip
> swap
> move
> mult
> remove
> removerange
> shuffle
> clear
> loop

**Player manipulations**
> pause
> resume
> exit

**Other**
> save
> ping
""",
	"ping": """```python
/ping
```
> Check bot responce""",
	"play": """```python
/ping
```
> Check bot responce""",
	"playing": """```python
/playing
```
> Show current playing song""",
	"playlist": """```python
/playlist [name : str]
```
> Add songs from playlist to end of queue and play
> 
> `name : string` - **Required argument**
> Playlist name""",
	"playepisode": """```python
/playepisode [eid : int]
```
> Rewind to episode in current playing song
> 
> `eid : int` - **Required argument**
> Episode ID, you can check in in queue (use `/queue`)""",
	"jump": """```python
/jump [qid : int]
```
> Skip current playing song and play song ar position `qid`
> 
> `qid : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)""",
	"skip": """```python
/skip
```
> skip current playing song""",
	"remove": """```python
/remove [qid : int]
```
> Remove song from queue in `qid` position
> 
> `qid : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)""",
	"removerange": """```python
/removerange [a : int] [b : int]
```
> Remove songs in positions from position `a` to position `b` (including both)
> 
> `a : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)
> `b : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)""",
	"swap": """```python
/swap [a : int] [b : int]
```
> Swap songs in positions `a` and `b` (including both)
> 
> `a : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)
> `b : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)""",
	"move": """```python
/move [a : int] [b : int]
```
> Move song from position `a` to position `b` (including both)
> 
> `a : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)
> `b : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)""",
	"queue": """```python
/queue
```
> Write queue""",
	"shuffle": """```python
/shuffle
```
> Shuffle queue""",
	"loop": """```python
/loop (single : bool)
```
> Loop queue, or unloop if alredy looped
> 
> `single : bool` - **Unrequred argument, standart value is** `False`
> if `True` only corrent song will be in endless loop""",
	"clear": """```python
/clear
```
> clear queue""",
	"mult": """```python
/mult [qid : int] [mult : int]
```
> Multiply song in position `qid` `mult` times
> 
> `qid : int` - **Required argument**
> Song ID (position in queue) you can check in in queue (use `/queue`)
> `mult : int` - **Required argument**
> Multiplier""",
	"pause": """```python
/pause
```
> Pause player""",
	"resume": """```python
/resume
```
> Resume player""",
	"save": """```python
/save [name : str] (overwrite : bool = False)
```
> Save songs from queue to playlist
> 
> `name : string` - **Required argument**
> Playlist name
> 
> `overwrite : bool` - **Unrequred argument, standart value is** `False`
> If `True` overwrite playlist if it`s already exist""",
	"exit": """```python
/exit
```
> Kill player"""
}