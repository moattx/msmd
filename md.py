#!/bin/python

import sys
import os
from yt_dlp import YoutubeDL

# TODO: if something already exists warn about it already existing then skip it
# (in parse() maybe?)


class Client:
    def __init__(self):
        self.playlists = []
        self.ytd_file_name = ""
        self.current_dir = os.getcwd()

    def run(self):
        with open("md.conf", "r", encoding="utf8") as file:
            self.parse(file)

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
        # finally change back to the previos directory TODO: check if this is
        # neccesary
        os.chdir("..")

    def parse(self, file):
        for i in file:
            if i == "\n":
                continue
            if i[0] == "#":
                # TODO: is there any better way to do this?
                # dont strip hashtag because it's needed in run() to check
                # whether it's a playlist or not
                self.playlists.append(i.strip("\n"))
                print(self.playlists)
                continue

            lst = i.split(" ")
            self.playlists.append(lst[0])
            self.playlists.append(lst[1].strip("\n"))

    def my_hook(self, d):
        if d["status"] == "finished":
            self.ytd_file_name = d["filename"]


def main():
    try:
        cli = Client()
        cli.run()
    except KeyboardInterrupt:
        sys.exit()


# MAIN
if __name__ == "__main__":
    main()
