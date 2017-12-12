"""
	Utility written to help organize my music files.
	Lowercases all title/album words in no_upper,
	moves songs into folders if not in one already.
	USE MUSIC - COPY FIRST
	Tim Coutinho
"""

import os
import re
from mutagen.easyid3 import EasyID3

no_upper = ('a', 'an', 'and', 'at', 'but', 'by', 'for','from',
			'in', 'nor', 'of', 'on', 'or', 'the', 'to')
good_ext = ('.aiff', '.ape', '.asf', '.flac', '.mp3', '.mp4', '.mpc',
			'.ofr', '.oga', '.ogg', '.ogv', '.opus', '.spx', '.tta', '.wv')
roman_nums = ('Ii', 'Iii', 'Iv', 'Vi', 'Vii', 'Viii', 'Ix')
base = '/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy'


def main():
	os.chdir(base)
	for artist in os.listdir():
		os.chdir(f'{base}/{artist}')
		print(artist)
		for album in os.listdir():
			if os.path.isfile(album):  # Create Unknown Album folder
				album = make_unknown(artist, album)
			modify_album(artist, album)


# Moves a song from the artist folder to an Unknown Album folder
def make_unknown(artist, song):
	os.mkdir('Unknown Album')
	os.rename(f'{base}/{artist}/{song}',
			  f'{base}/{artist}/Unknown Album/{song}')
	return 'Unknown Album'


# Modifies all valid audio files in an album
def modify_album(artist, album):
	os.chdir(f'{base}/{artist}/{album}')
	for song in os.listdir():
		song = os.path.splitext(song)
		if song[1] in good_ext:  # Valid audio extension
			modify_song(song)


# Modifies a song's title and album tags
def modify_song(song):
	audio = EasyID3(''.join(song))
	try:					# In an album, tag exists
		modify_tag(song, audio, 'album')
	except Exception:		# Not in an album, tag does't exist
		pass
	if 'title' not in audio:  # Use file name as title
		# Removes any leading album identifiers, i.e. 01 and 13 -
		audio['title'] = re.sub(r'^([0-2]?[\d][^\d,]) ?\-?\.? ?\-?',
								'', song[0].lstrip('0'))
	modify_tag(song, audio, 'title')
	audio.save()


# Changes a specific tag of a song, either title or album
def modify_tag(orig, audio, tag):
	audio[tag] = re.sub(r'(\w+)(/)(\w+)', r'\1 / \3', audio[tag][0]).lower()
	audio[tag] = ' '.join([word if re.sub(r'[:/\-]', '', word)
						   in no_upper else word.capitalize()
						   for word in audio[tag][0].split()])
	if any(word.strip(':') in roman_nums for word in audio[tag][0].split()):
		for word in audio[tag][0].split():
			if word.strip(':') in roman_nums:
				audio[tag] = audio[tag][0].replace(word, word.upper())
	c = '_'
	while '_' in audio[tag][0]:
		c = input(f'What character should replace the _ in {audio[tag][0]}? ')
		audio[tag] = audio[tag][0].replace('_', c, 1)
	# Capitalize the first word regardless
	audio[tag] = audio[tag][0][0].upper() + audio[tag][0][1:]
	# sub = re.sub(r"[/:\?]", "_", audio[tag][0])
	# if tag == 'title' and 'album' in audio:  # Rename file to new song title
	# 	os.rename(f'{base}/{audio["artist"][0]}/{audio["album"][0].replace("/", "_")}/{"".join(orig)}',
	# 			  f'{base}/{audio["artist"][0]}/{audio["album"][0].replace("/", "_")}/{sub}{orig[1]}')
	# 	# os.remove(f'{base}/{audio["artist"][0]}/{audio["album"][0].replace("/", "_")}/{"".join(orig)}')
	# elif tag == 'title':
	# 	os.rename(f'{base}/{audio["artist"][0]}/Unknown Album/{"".join(orig)}',
	# 			  f'{base}/{audio["artist"][0]}/Unknown Album/{sub}{orig[1]}')
	# 	# os.remove(f'{base}/{audio["artist"][0]}/Unknown Album/{"".join(orig)}')


if __name__ == '__main__':
	main()