import pytube

video = pytube.YouTube("https://www.youtube.com/watch?v=iiw9Z1I1AcE")
print("ds")



for i in range(len(video.fmt_streams)):
	print(i, video.fmt_streams[i])

video.fmt_streams[int(input("choose stream: "))].download()

print("dd")