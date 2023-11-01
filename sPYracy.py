import youtube_search
import yt_dlp
import os; os.system("")
import time
import json
from tkinter import filedialog
import sys
sys.stdout = open(os.devnull, "w").close()
import pygame
sys.stdout = sys.__stdout__

print("\033[38;2;0;255;100msPYracy   for Windows   is loading...")
songs = []
pygame.mixer.init()
songIndex = 0
# load animation keys
keys = []
try:
    f = open("config.spyc", "r")
    for l in f.read().split("Animation: ")[1].split(" SPY")[0]:
        keys.append(l)
    f.close()
except Exception as e:
    f = open("config.spyc", "w")    
    f.write("Animation: #~ SPY\nvExtensions: flac,mp3,ogg SPY")
    f.close()
    keys = ["#", "~"]
    print(e)

debug = True
errors = {
    "wronginput": "Incorrect integer input value!"
}

def search(song : str):
    print("\033[38;2;0;255;100mSearching...")
    unsplit = youtube_search.YoutubeSearch(search_terms=song, max_results=1).to_json()
    print("\033[38;2;0;255;100mSong found, grabbing id...")
    beforeid = unsplit.split("id\": \"")[1]
    return beforeid.split("\", \"")[0]

class Logger:
    def debug(self, msg):
        if not msg.startswith('[debug] '):
            self.info(msg)
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self,msg): print("\033[38;2;0;255;100mERROR: %s" % msg) 

status = 0
def hook(d):
    global status
    if d["status"] == "downloading":
        if round(float((d['downloaded_bytes'] / d['total_bytes'])) * 100) >= round(status) + 10:
            sec = round(round(float((d['downloaded_bytes'] / d['total_bytes'])) * 100) / 10)
            print("\033[38;2;0;255;100m\033[-%sC" % sec, end="")
            [print(keys[0], end="") for _ in range(sec)]
            print("\033[38;2;0;255;100m\033[%sD" % sec, end="") 
        # print(f"Downloading video... speed: {d['speed']}, time elapsed: {d['elapsed'] / 1000}, percent downloaded {float((d['downloaded_bytes'] / d['total_bytes'])) * 100}%)")

def download(id: str):
    print("\033[38;2;0;255;100m[%s]" % "".join(keys[1] for i in range(10)), end="")
    print("\033[38;2;0;255;100m\033[11D", end="")
    config = {"outtmpl": "%(title)s",
        "format": "bestaudio/best",
        "progress_hooks": [hook],
        "logger": Logger(),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio","preferredcodec": "flac",
                }
                ],
            }

    yt_dlp.YoutubeDL(config).download(id)

def getSongExtensions():
    try:
        with open("config.spyc") as f:
            print(f.readlines())
    except Exception as e:
        print(e)

def executeOption(option):
    global keys, songs, songIndex
    prvmsg = None
    animations = [
        "#~",
        "#-",
        "o-",
        "o~",
    ]
    if option >= 1 and option <= 15:
        print("\033[38;2;0;255;100m\n", end="")
    else:
        print("\033[38;2;0;255;100mThis option does not exist!")
    if option == 1:
        song = input("Song Name: ").encode()
        songID = search(song=song)
        print("\033[38;2;0;255;100mDownloading With ID: %s" % songID)
        download(songID)
        prvmsg = "Downloaded song \"%s\"" % song.decode()
    elif option == 2:
        try:
            pygame.mixer.music.unload()
        except: ...
        songs.clear()
        songIndex = 0
        for file in filedialog.askopenfilenames():
            songs.append(file)
        pygame.mixer.music.load(songs[songIndex])
        for song in songs:
            pygame.mixer.music.queue(song)
        pygame.mixer.music.play()
        songIndex += 1
    elif option == 3:
        currentAnimation = "[%s]" % ("".join(["".join(keys[0]) for i in range(3)]) + "".join(["".join(keys[1] for i in range(2))]))
        print("\033[38;2;0;255;100m\n== Animation Changer ==\n\nCURRENT: %s\nAnimation 1: [####~~]\nAnimation 2: [###--]\nAnimation 3: [ooo--]\nAnimation 4: [ooo~~]\nAnimation 5: CUSTOM" % currentAnimation)
        newAnimation = int(input("Input Animation (INT): "))
        if 1 > newAnimation or newAnimation > 5:
            print("\033[38;2;0;255;100mInvalid Option") 
        else:
            if 5 >= newAnimation >= 1: 
                f = open("config.spyc", "r+")
                content = f.read()
                getAnimation = content.split("Animation: ")[1].split(" SPY")[0]
                f.seek(0)
                f.truncate()
                keys.clear()
                loadingAnimation = ""
                try:
                    for l in animations[newAnimation-1]:
                        keys.append(l)
                    loadingAnimation = animations[newAnimation-1]
                except:
                    if debug: ...
                if newAnimation == 5:
                    loadingAnimation = input("First part of animation (???~~): ") + input("Second part of animation (###??): ")
                    keys.clear()
                    for l in loadingAnimation:
                        keys.append(l)
                f.write(content.replace("Animation: " + getAnimation + " SPY", "Animation: %s SPY" % loadingAnimation))
                print("\033[38;2;0;255;100mAnimation has been changed to: [%s]" % ("".join(["".join(keys[0]) for i in range(3)]) + "".join(["".join(keys[1] for i in range(2))])))
                f.close()  
    elif option == 4:
        print(open("config.spyc", "r").read())
    elif option == 5:
        with open("config.spyc", "r") as f:
            print(f.read().split("vExtensions: ")[1].split("SPY")[0])
    elif option == 6:
        pygame.mixer.music.pause()
    elif option == 7:
        pygame.mixer.music.unpause()
    elif option == 8:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(songs[songIndex])
        pygame.mixer.music.play()
        songIndex += 1
    elif option == 9:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(songs[songIndex-2])
        pygame.mixer.music.play()
        songIndex -= 2
    elif option == 10:
        print(pygame.mixer.music.get_busy())
    elif option == 11:
        pygame.mixer.music.load("Anthem.flac")
        pygame.mixer.music.play()
    elif option == 12:
        print("\033[39m") 
        sys.exit()
    elif option == 13:
        print(len(songs))
    elif option == 14:
        pygame.mixer.music.set_pos(float(input("Seek position: ")))
    elif option == 15:
        pygame.mixer.music.rewind()
    previewOptions(prvmsg)


def previewOptions(previewmessage=None):
    print("\033[38;2;0;255;100m\nsPYracy   for Windows   - vBETA 1")
    options = [
        "Download Song",
        "Queue Songs",
        "Change Download Animation",
        "Read config.spyc ",
        "Read valid song extensions from config.spyc ",
        "Pause",
        "Resume",
        "Skip",
        "Reverse",
        "Get business of pygame ",
        "Play test audio ",
        "Exit",
        "Get Songs len ",
        "Seek",
        "Restart Song"
    ]
    if previewmessage != None:
        print("\033[38;2;0;255;100m\n\n")
        print(previewmessage)
    [print("\033[38;2;0;255;100mOption #%s - %s" % (_ + 1, __)) for _, __ in enumerate(options)]
    grabInput = int(input("Input Option (int): "))    
    executeOption(grabInput)
print("\033[38;2;0;255;100msPYracy has completed loading\n")
print("\033[38;2;0;255;100m⢳⢕⢇⢗⢕⢇⢗⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⠕⡕⢕⠕⡕⢕⠕⡕⢕⠕⡕⢕⢕⠕⡕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⢕⡕⡵⡱⡣⡳⡱⣣⢳⡹⡜⣎⢗⢵\n⢇⢗⢝⢜⢕⢕⡕⡕⡕⡕⡕⡕⡕⢕⢅⢇⢎⢆⢇⠇⡇⢇⢣⠣⡣⢣⠣⡣⢣⢣⢱⠱⡱⡑⡕⡜⡔⡕⡜⡔⢕⢱⢸⢰⠱⡡⡣⡱⡡⡣⡱⣱⣵⣷⣷⣧⡇⡇⡇⡇⡇⡇⡇⡇⡇⡗⡝⡜⡎⡮⣪⢺⢜⢎⢧\n⡸⡱⡹⡸⡱⡱⡱⡱⡱⡱⡑⡕⡜⢜⢌⢆⢇⠎⡆⢇⢣⠣⡃⡇⡣⡃⡇⡣⡣⡱⡸⡘⡌⡎⡪⡢⢣⠪⡢⢣⠣⡣⡱⡪⡪⢪⢸⢨⢪⠸⣸⣳⣿⣿⣿⣿⣿⡎⡜⡌⡎⢎⢎⢎⢮⢪⢪⢪⢺⢸⢜⢎⢮⢳⢹\n⢮⢪⢣⢣⢣⢣⠣⡣⡱⡸⡘⡌⣎⣮⣮⣶⣷⣷⣷⣷⣷⣧⣧⣕⢅⢇⢕⠕⡜⢔⢅⢇⢕⢅⠇⡎⡪⡊⡎⡪⡊⡎⢜⢻⣎⢎⠆⡇⢎⢎⢺⡏⡎⡽⡇⡝⣏⢇⢇⢕⠕⡕⣅⣷⢏⢎⢎⢎⢎⢎⢮⢺⢸⢪⡣\n⡣⡣⡣⡣⡣⡣⡣⢣⠣⣱⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣔⣕⢱⢑⠕⡜⢔⢕⢱⢑⢅⢇⢕⢅⢇⢎⢎⢪⢹⣷⣕⢕⢱⠡⡝⡻⣿⣭⣻⡾⡟⡢⡣⢪⢊⣮⣾⡓⡕⢕⢱⢱⢱⢱⢱⢱⢕⢇⢗\n⡜⡜⡜⡜⡜⡌⡎⣮⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡪⡊⡎⡪⢢⢣⠱⡡⡣⢪⠢⡣⢪⢸⢨⢢⡙⡻⣷⣵⡑⡕⢽⣚⣻⠫⣺⢜⢌⢎⣮⣾⢟⢕⢜⠜⡜⢜⢜⢸⢸⢸⢸⢸⢜⢎\n⢜⢜⢜⢜⢔⢵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⢌⢎⢪⠢⡣⢣⠪⡊⡎⡪⡊⡆⢇⢕⠜⡜⢜⢻⣯⡪⣎⡻⠶⡟⢇⡧⣞⡿⡻⡱⡑⡕⢜⢜⢸⢘⢌⢎⠎⡎⡎⡎⡎⡮\n⢇⢇⢇⢕⢬⣿⣿⣿⡿⡿⡻⡛⡟⡫⡫⡹⡩⡫⡛⡻⡛⡟⡿⢿⣿⣿⣿⣿⣿⣿⣿⣎⢎⠆⡇⡣⡃⡇⡣⡱⡡⡣⡱⡑⡅⡇⡝⡕⡱⡰⣙⡳⢭⡺⡜⣕⢏⢇⢣⢱⢪⢪⢊⢎⢢⢣⢱⢑⢅⢇⢣⠣⡣⡣⡣\n⢕⢕⢕⢱⣿⣿⣿⣿⢸⢨⢢⢣⢱⣱⣸⣰⣱⣨⣪⡸⡨⡢⢣⠣⡊⡎⡛⠿⣿⣿⣿⣿⡜⡜⡌⢎⢪⢸⢨⠪⡢⢣⠪⡊⡎⡪⡢⡣⡣⢝⢢⢓⢕⢜⢜⢪⠪⡕⡕⡕⡕⢕⢱⢡⢣⢱⠸⡨⡪⡸⡨⡪⢪⢪⢪\n⡪⡢⡣⣹⣿⣿⣿⣿⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣵⣑⢕⢕⢢⣿⣿⣿⣯⢢⠣⡣⢣⠱⡡⡣⡃⡇⡣⣣⣧⣧⣮⣊⢮⣎⢎⢪⡦⡣⡪⡊⡎⡪⡸⡨⡪⢪⢊⢎⢢⢃⢇⢕⢜⠔⡕⢜⠜⡔⡕\n⡣⡱⡑⣿⣿⣿⣿⣿⣿⢻⢙⢍⢇⠎⡆⡕⡜⢔⢱⢩⠫⡛⡻⠿⣿⣿⣿⣾⣾⣿⣿⣿⣿⢕⢕⢱⢑⢕⠕⡜⣾⡻⢗⢼⣿⣢⣹⡿⡨⡻⣾⡟⡕⣿⡿⢇⢻⣛⢷⣕⣼⡞⡟⡷⡹⣧⢣⣿⢱⢑⢕⢱⢑⢕⢕\n⠪⡊⡎⣿⣿⣿⣿⣿⣿⣼⣼⣬⣶⣷⣷⣾⣾⣾⣾⣦⣧⣣⡣⡹⡨⢍⠿⣿⣿⣿⣿⣿⣿⢕⢇⢇⢕⢅⢇⢕⣭⣻⡷⣺⣿⡙⡝⢜⢌⢎⣿⢪⠪⣿⣏⠪⣿⣹⣽⡧⡻⣧⣣⡮⣘⢻⣽⢇⢣⢱⢡⢣⢱⢱⢱\n⡪⡪⡪⢺⣿⣿⣿⣿⣿⣿⡿⢿⠿⢟⢻⢛⢟⢻⢻⠿⣿⣿⣿⣿⣾⣬⣾⣿⣿⣿⣿⣿⡿⡱⡝⣜⢔⢕⠜⡌⢎⢕⢕⢢⢢⢣⠪⡪⢢⠣⡪⡢⢣⠣⡒⡍⢎⢕⠜⡌⢎⢪⢙⢌⠶⢿⢫⠪⡊⡆⡇⡕⡕⢕⢕\n⡸⡨⡪⡪⣿⣿⣿⣿⣿⣇⣇⣣⣭⣮⣮⣮⣼⣬⣦⣓⣔⠬⡹⡹⠿⣿⣿⣿⣿⣿⣿⣿⢏⢞⡜⡎⡮⡢⡣⢣⠣⡱⡸⢰⠱⡸⡘⡜⡌⡎⢆⢇⢣⢃⢇⢕⠕⡅⢇⢣⠣⡃⡇⡕⢕⢕⢱⢑⢕⠕⣼⣜⢜⢜⢜\n⡜⡜⡌⡎⣚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣼⣸⣿⣿⣿⣿⣿⣿⢯⢫⢕⢝⡜⡵⡱⡕⢕⢍⢎⢪⢱⢩⠪⡊⡎⡪⢪⠱⡑⡕⢕⢱⢑⢍⢎⢕⠕⡍⡎⡪⡪⡱⡑⡕⢕⠕⡍⣛⢏⢎⢎⢎\n⡪⡪⡪⡊⡆⢞⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡫⣣⢳⢱⡣⡳⡱⡣⡫⡪⡢⢣⠱⡑⡜⢜⢌⢎⢪⢊⢎⢪⣾⢿⣾⡜⡔⢕⠜⣜⢌⢎⢜⠔⡕⢜⢸⢘⢜⢜⢔⢕⢕⢕⢕\n⡸⡸⡸⡘⡜⡜⡌⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⢱⢕⢵⢱⢣⢳⢹⡸⣱⢹⡸⡸⡘⡜⢜⢸⢨⠪⡣⢣⠱⡑⠽⣿⣽⣿⢗⢕⢱⠱⡸⡑⡕⢜⢸⢘⢜⢌⢎⢆⢇⢕⢕⢕⢕⢝\n⡎⡎⡎⡎⡎⡆⡇⡎⡎⡟⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⢏⢗⢕⢇⢗⢵⢹⢜⢕⢵⡱⡕⡵⣱⢹⡸⡘⡜⡌⡆⡇⢇⢣⠣⡣⡋⡎⢝⢱⠱⡸⡰⡱⡑⡕⢜⢜⢌⠎⡆⢇⢕⢜⢜⢜⢜⢜⢜⢎\n⢎⢮⢪⢪⢪⢊⢆⢇⢎⢎⢮⢪⡫⡻⡻⢿⢿⢿⢿⢿⢿⢻⢻⡹⡪⡣⡳⡹⣸⢱⢝⢜⢎⢮⢣⢇⢧⢳⢹⢸⢜⢼⢸⢰⠱⡘⡜⡸⡨⡪⡢⢣⠪⡪⡊⡎⢆⢣⢪⢸⢨⠪⡢⡃⡇⡣⡣⡣⡣⡣⡣⡣⡣⡳⡱\n⡕⣇⢧⢣⢣⢣⢣⢣⢱⢸⠸⡸⡜⡎⡮⡣⡣⡇⡧⣣⢳⢹⡸⡜⡎⣇⢏⢞⢜⢎⡎⡧⡫⣪⢺⡸⡪⣪⢣⡳⡱⡣⡳⡱⡱⡑⡕⡱⡸⢰⢑⢕⢱⢡⠣⡪⡪⡊⡆⢇⢕⠕⡅⡇⡣⡣⡣⡪⡪⡪⡪⡪⣪⢣⡫\n⡱⡕⡵⡱⡕⣕⢕⢕⢕⢕⢕⢕⢕⢝⡜⡎⣇⢏⢮⢪⢎⢇⢧⢣⡫⣪⢪⡣⣫⢪⢎⢞⡜⣎⢮⢪⡺⡸⣱⢱⡹⡜⣕⢝⡜⡌⡎⡜⡌⡎⡪⡸⡨⡢⡣⡣⢪⢪⢸⢸⢰⢱⠱⣑⢕⢕⢜⢜⢜⢜⢜⢎⢮⡪⡺\n⡕⣝⢜⡎⡮⡪⣪⢪⢪⢪⢪⢪⢪⢪⡪⡺⡸⡪⡣⡳⡱⡝⣜⢕⡕⡵⡱⣕⢕⢇⡏⡮⡪⡎⣎⢇⢧⢫⡪⡎⡮⡪⡎⡮⡪⡎⡎⡆⡇⡕⢕⢅⢇⢕⢜⠜⡜⢔⢕⢕⢜⢜⢜⢔⢕⢕⢕⢕⢵⢹⡸⡱⣕⢵⢝")
previewOptions()
