import pytube

lst = [1, 2, 3]
video = pytube.YouTube("https://www.youtube.com/watch?v=OkFGoSUdli0")

print(video.thumbnail_url)
print(video.channel_url)
