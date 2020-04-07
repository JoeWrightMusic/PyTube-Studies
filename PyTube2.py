from __future__ import unicode_literals
import urllib.request
import urllib.parse
import re
import os
import youtube_dl
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
from random import uniform, random, randint
import time
import datetime
# FFMPEG also needed for some scripts to run!

#EDIT VALUES TO DETERMINE LENGTH AND CONTENT OF OUTPUT
squaresize = 32
iterations = 100
word_array = ['pie', 'metal tube', 'pvc tube', 'pastry crust']
x=0
delete_temps=-1
while x < iterations:
    print('BEGIN'+str(x)+'/////////////////////')
    search_res = 0
    search_string = word_array[x%len(word_array)]
    print(search_string)
    query_string = urllib.parse.urlencode({"search_query" : search_string})
    #search for results <4min
    html_content = urllib.request.urlopen("https://www.youtube.com/results?" + 'sp=EgQQARgB&'+ query_string)
    time.sleep(0.5)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    time.sleep(0.5)
    
    try:
        if len(search_results) > 2:
            search_res = randint(0, (len(search_results)-1))
        else: 
            search_res = 0

        full_url = "http://www.youtube.com/watch?v=" + search_results[search_res]
        print('URL:' + full_url + ' RESULT No. ' + str(search_res))
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta =  ydl.extract_info(full_url , download=False) 
            vidlength = meta['duration']
        vidlength = vidlength/2
        print(meta['title']) 
        s=meta['title']
        go2dl = 1
    except:
        go2dl = 0

    if go2dl==1: 
        try:
            cur_ytvid = 'temp'+str(x)+'.mp4'
            
            ydl_opts = {
                'outtmpl': cur_ytvid, 
                'no-playlist': 'true',
                'format': 'best[ext=mp4]',
            }
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([full_url]) 
                time.sleep(0.5)
                print("Video downloaded!")
            clip = 1
        except: 
            print("Mp4 not available, trying something else...")
            clip = 0

        if clip == 1:
            try: 
                # load to videoFileClip and get duration
                fullvideo = VideoFileClip(cur_ytvid)
                vidlength = fullvideo.duration
                # get random length and start point
                if vidlength <= 2: 
                    start = 0
                    length = 0.1
                else: 
                    length = round(uniform(0.1,0.99), 2)
                    start = round(uniform(0, vidlength-2), 2)
                print([vidlength, start, length])
                vidclip = fullvideo.subclip(start, start+length)
                print('Got clip')
                time.sleep(0.5)
                join=1
            except: 
                os.remove(cur_ytvid)
                print('Corrupted d-l')
                join=0
            
            if join == 1:
                try:
                    # join and store video clips
                    if x==0:
                        vidclip.write_videofile('Output0.mp4')
                        print('Output done!')
                        time.sleep(0.5)
                    else: 
                        previous = VideoFileClip('Output'+str(x-1)+'.mp4')
                        vidout = concatenate_videoclips([previous, vidclip])
                        vidout.write_videofile('Output'+str(x)+'.mp4')
                        print('Output done!')
                        time.sleep(0.5)
                    x+=1
                    delete_temps=1
                except:
                    print("File read error - rewinding from "+str(x))
                    x -= 1
                    print('REWIND TO: ' + str(x))
                    delete_temps=0
            if delete_temps == 1:
                print('removing: ' + cur_ytvid)
                os.remove(cur_ytvid)
                try:
                    if x>2:
                        print('Removing: Output'+str(x-3)+'.mp4')
                        os.remove('Output'+str(x-3)+'.mp4')
                        print('Videos removed')
                except: 
                    print('Old video already deleted, moving on...')
print(('Output'+str(x-1)+'.mp4'))
finalvideo = VideoFileClip('Output'+str(x-1)+'.mp4')
time.sleep(2)
wid = finalvideo.w
hgt = finalvideo.h
wid = randint(0, (wid-squaresize))
hgt = randint(0, (hgt-squaresize))
print([wid, hgt])
finalvideo = finalvideo.fx( vfx.crop,wid,hgt,wid+squaresize,hgt+squaresize)
finalvideo = finalvideo.resize( (800,800) ) 
finalvideo.write_videofile('FinalVid0.mp4')
#keep a copy pre-sharpening to preserve audio
finalvideo.write_videofile('FinalVid.mp4')
os.remove('Output'+str(x-1)+'.mp4')
os.remove('Output'+str(x-2)+'.mp4')
#sharpen 100x
for x in range(100):
   os.system("ffmpeg -i FinalVid" + str(x) + ".mp4 -filter:v \"unsharp=13:13:5:13:13:5\" FinalVid" + str(x+1) + ".mp4")
   os.remove("FinalVid" +str(x)+ ".mp4")


