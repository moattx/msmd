# msmd - moatx's stupid music downloader

This music downloader works by utilizing playlists, and it also uses a configuration file that holds links to music and names for that music.

The music downloader parses md.conf in the current working directory, and then from the info gotten from md.conf, it'll download the links using yt-dlp with the specified name in the specified playlist (which is just a directory)

## The configuration file - md.conf

The way md.conf works is pretty simple. If there is a hashtag, then everything that comes after it is the playlist's name, and everything under it is the music that belongs to that playlist.

Songs in a playlist are identified by the link to the music that you want to download, and then after the link that was specified, you specify what you want to call the music that's being downloaded.

example:

    #hip hop
    https://www.youtube.com/watch?v=dQw4w9WgXcQ nice

In this example, "hip hop" is the playlist, and then under the playlist, https://www.youtube.com/watch?v=dQw4w9WgXcQ is the link to the music that md.py will download, and right next to the link is the name of the music, which will be "nice.mp3" (md.py uses mp3 by default; this will change later)
