import _thread
import time
from pytube import YouTube
from pytube import Playlist
import os
import re



def downloadVideo(video, count):
    retry = 0
    global noofthreds, dirName
    global summeryText, summerySuccess, summeryLowQuelity, summeryError

    filename = video.title
    filename = re.sub('[^A-Za-z0-9 ]+', '', filename)
    filename = filename+ ".mp4"
    newfilename = str(count)+ " - " + video.title+ ".mp4"
    print(newfilename)
    
    try:
        result = video.streams.get_by_itag(22).download(dirName)
        filename = os.path.basename(result)
        newfilename = str(count)+" - "+filename
        os.rename(os.path.join(dirName, filename), os.path.join(dirName, newfilename)) 
        print(newfilename+", success")
        summerySuccess += newfilename+", success\n"
    except:
        try:
            result = video.streams.first().download(dirName)
            # print(result)
            filename = os.path.basename(result)
            newfilename = str(count)+" - "+filename
            # os.rename(filename, newfilename)
            os.rename(os.path.join(dirName, filename), os.path.join(dirName, newfilename))
            print(newfilename+", low quelity, success")
            summeryLowQuelity += newfilename+", low quelity, success\n"
        except:
            print()
            # os.remove(filename)
            retry += 1
            success = 0
            while retry < 4:
                try:
                    result = YouTube(video.watch_url).streams.first().download(dirName)
                    filename = os.path.basename(result)
                    newfilename = str(count)+" - "+filename
                    # os.rename(filename, newfilename)
                    os.rename(os.path.join(dirName, filename), os.path.join(dirName, newfilename))
                    print(newfilename+", low quelity, success")
                    summeryLowQuelity += newfilename+", low quelity, success\n"
                    success = 1
                    break
                except:
                    retry += 1
            if success == 0:
                print(newfilename+", Error, "+ video.watch_url +" \n\n") 
                summeryError +=  newfilename+", Error, "+ video.watch_url +" \n"

    noofthreds -=   1

# YouTube('https://www.youtube.com/watch?v=rpepyyhclsQ&list=PLO3amA80qH2MmEUonQk_UaMVCF2jzuLIb').streams.first().download()
# p = Playlist('https://www.youtube.com/watch?v=rpepyyhclsQ&list=PLO3amA80qH2MmEUonQk_UaMVCF2jzuLIb')

print("=============== YouTube playlist download ============")
plist = input("Enter the url of play list:")

p = Playlist(plist)

print(f'Downloading: {p.title}')
dirName = p.title
dirName = re.sub('[^A-Za-z0-9 ]+', '', dirName)
os.mkdir(dirName)

summeryText = "=========== Summery =========\n"
summerySuccess = ''
summeryLowQuelity = ''
summeryError = ''



count = 1
noofthreds = 0
maxnoofthreats = int(input("No of threats : ") or "3")

startFrom = int(input("Start from(you already downloaded fes videos) : ") or "1")

for video in p.videos:    
         

    try:
        if(count < startFrom):
            count = count + 1
            continue
        _thread.start_new_thread( downloadVideo, (video, count, ) )
        noofthreds = noofthreds + 1
        
    except:
        print("Error: unable to start thread")

    while noofthreds > maxnoofthreats-1:
        time.sleep(1)

    count = count + 1


while noofthreds > 0:
    time.sleep(5)


summeryText = summeryText + "\n\nSuccess >>>>>\n" + summerySuccess + " \n\nLow Quelity >>>>\n" + summeryLowQuelity + "\n\nErrors >>>>\n" + summeryError

summaryFileName = str(p.title)+".txt"
summeryFile = open(os.path.join(dirName,summaryFileName), "w")
summeryFile.write(summeryText)
summeryFile.close()



