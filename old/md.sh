#!/bin/bash

# TODO: make it way better
# TODO: add options like -o which redirects download to a dir
#
# AUXILIARY FUNCTIONS

# display an error message to stderr (in red)
err() {
	printf "\33[2K\r\033[1;31m%s\033[0m\n" "$*" >&2
}

# displays info (in green)
inf() {
	printf "\033[1;32m%s\033[0m\n" "$1"
}

# display error message and exit
die() {
	err "$*"
	exit 1
}

# checks if dependencies are present
dep_ch() {
	for dep; do
		if ! command -v "$dep" >/dev/null; then
			die "Program \"$dep\" not found. Please install it."
		fi
	done
}

download() {
	#TODO: let user decide on the formats and stuff
	yt-dlp -f 'bestaudio/best' -w -o "$2.%(ext)s" -v -x --audio-format flac "$1"
}

# parses a file that has the link and name to the music
parse() {
	shopt -s lastpipe # XXX: I DONT LIKE THIS TODO: REMOVE THIS (POSIX?)
	n=0
	grep -v '^ *#' <"$1" | while IFS= read -r line; do

		read -ra arr <<<"$line"

		links[$n]=${arr[0]}
		names[$n]=${arr[1]}

		n=$((n + 1))

	done

	shopt -u lastpipe
}

# TODO: explain what main does in steps
main() {
	#set -e

	#inf "Checking dependencies.."

	# requires yt-dlp
	#dep_ch "yt-dlp"
	parse "md.conf"

	for ((n = 0; n < ${#links[@]}; n++)); do
		inf "link = ${links[$n]} name = ${names[$n]}"
		inf "Downloading music..."
		download "${links[$n]}" "${names[$n]}"
	done
}
main "$@"
