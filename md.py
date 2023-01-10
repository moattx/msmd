#!/bin/python

import sys
import os
from yt_dlp import YoutubeDL


class Client:
    def __init__(self):
        self.playlists = []
        self.ytd_file_name = ""
        self.current_dir = os.getcwd()

    def run(self):
        self.parse()
        print("playlist = ", self.playlists)

        number = 0

        while number != len(self.playlists):

            # hastag for playlist (directory)
            if self.playlists[number][0] == "#":
                if os.getcwd() != self.current_dir:
                    os.chdir(self.current_dir)

                playlist_name = self.playlists[number].strip("#")
                print("creating a playlist named " + playlist_name + "...")
                os.mkdir(playlist_name)
                os.chdir(playlist_name)
                number = number + 1
                continue

            ydl_opts = {
                "format": "m4a/bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "m4a",
                    }
                ],
                "progress_hooks": [self.my_hook],
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.playlists[number]])

            number = number + 1
            file_name = self.playlists[number] + ".mp4"

            # update to go to next link or playlist name
            number = number + 1

            print("FILE_NAME = " + self.ytd_file_name)
            if len(self.ytd_file_name) != 0:
                os.rename(self.ytd_file_name, file_name)
        # finally change back to the previos directory
        # TODO: check if this is neccesary
        os.chdir("..")

    def parse(self):
        # tmplist = []
        skip = False
        # TODO: find a better way to get home dir?
        with open(os.environ["HOME"] + "/.md.conf", "r", encoding="UTF-8") as file:
            lines = list(line for line in (l.strip() for l in file) if line)
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

    def my_hook(self, d):
        if d["status"] == "finished":
            self.ytd_file_name = d["filename"]


# MAIN
try:
    Client().run()
except KeyboardInterrupt:
    sys.exit()
