#!/bin/python

import sys
import os
from yt_dlp import YoutubeDL


class Client:
    def __init__(self):
        self.playlists = []
        self.playlist = ""
        self.ytd_file_name = ""
        self.path = os.getcwd()

    def run(self):
        self.parse()
        print("playlist = ", self.playlists)

        number = 0

        while number != len(self.playlists):

            # hastag for playlist (directory)
            if self.playlists[number][0] == "#":
                if self.playlist:
                    print("done with " + self.playlist + " making new playlist...")

                if os.getcwd() != self.path:
                    os.chdir(self.path)

                self.playlist = self.playlists[number].strip("#")
                print("creating a playlist named " + self.playlist + "...")
                os.mkdir(self.playlist)
                os.chdir(self.playlist)
                # skip playlist name
                number = number + 1
                continue

            # skip link
            number = number + 1
            file_name = self.playlists[number] + ".mp4"

            print("music = " + file_name + " for " + self.playlist)
            # if len(self.ytd_file_name) != 0:
            ydl_opts = {
                "format": "m4a/bestaudio/best",
                "outtmpl": file_name,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "m4a",
                    }
                ],
            }

            print("downloading music...")
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    # INFO: decrement for the link
                    ydl.download([self.playlists[(number - 1)]])
                except:
                    pass

            # update to go to next link or playlist name
            number = number + 1

        print("goodbye...")

    def parse(self):
        # tmplist = []
        skip = False
        # TODO: find a better way to get home dir?
        with open(os.environ["HOME"] + "/.md.conf", "r", encoding="UTF-8") as file:
            lines = list(line for line in (line.strip() for line in file) if line)
            for line in lines:
                if line[0] == "#":
                    playlist = line.strip("#")

                    if os.path.isdir(playlist):
                        print(playlist + " exists...skipping...")
                        skip = True
                    else:
                        skip = False

                    if not skip:
                        print(playlist + " is a playlist")
                        # INFO: do not use the playlist var because it strips
                        # '#' and '#' is needed in run()
                        self.playlists.append(line)

                    continue
                if not skip:
                    print("adding music for the playlist...")
                    # link
                    self.playlists.append(line.split(" ")[0])
                    # name
                    self.playlists.append(line.split(" ")[1])


# MAIN
try:
    Client().run()
except KeyboardInterrupt:
    sys.exit()
