"""
    Utility written to help organize music files.
    Lowercases all title/album words in NO_UPPER,
    moves songs into folders if not in one already.
    Supports: .aiff, .ape, .asf, .flac, .mp3, .mp4, .mpc,
    .ofr, .oga, .ogg, .ogv, .opus, .spx, .tta, and .wv
    USE MUSIC - COPY FIRST, run tests beforehand.
    Tim Coutinho
"""

import re
from pathlib import Path

from lib import open_audio


NO_UPPER = ('a', 'an', 'and', 'at', 'but', 'by', 'de', 'for',
            'from', 'in', 'nor', 'of', 'on', 'or', 'the', 'to')
EXCEPTIONS = {'adhd': 'ADHD', 'id': 'ID', 'sea is a lady': 'SEA IS A LADY',
              'i want! i want!': 'i want! i want!', 'cspan': 'CSPAN',
              'futuresex  /  lovesounds': 'FutureSex / LoveSounds',
              'nordo': 'NORDO', 'bad axe, mi': 'Bad Axe, MI'}
ROMAN_NUMS = ('Ii', 'Iii', 'Iv', 'Vi', 'Vii', 'Viii', 'Ix')

re_nums = re.compile(r'^[0-1]?[\d]\W[.\- ]*')
re_parens = re.compile(r'[([:.]+ *[a-z]')
re_spec = re.compile(r'[:/\-]')


def make_unknown(song_path):
    """Move a song from the artist folder to an Unknown Album folder."""
    unknown = song_path.parent / 'Unknown Album'
    unknown.mkdir()
    song_path.rename(unknown / song_path.name)
    return 'Unknown Album'


def modify_song(song):
    """Modify a song's title and album tags."""
    with open_audio(str(song)) as audio:
        print(str(song))
        try:
            old = dict(audio)
        except TypeError:  # Invalid file type
            return False
        try:
            album = audio['album'][0]
        except KeyError:  # Not in an album, tag doesn't exist
            pass
        else:
            audio['album'] = [modify_tag(album)]
        try:
            title = audio['title'][0]
        except KeyError:  # Use file name as title
            # Removes any leading album identifiers, i.e. '01' and '13 -'
            title = re_nums.sub('', song.stem)
        print(title)
        audio['title'] = [modify_tag(title)]
        return old != audio


def modify_tag(tag):
    """Change a specific tag of a song."""
    # Makes directory navigation easier, adding spaces around any /
    tag = tag.replace('/', ' / ').lower()
    if tag in EXCEPTIONS:
        return EXCEPTIONS[tag]
    tag = ' '.join([word if re_spec.sub('', word) in NO_UPPER
                    else word.capitalize() for word in tag.split()])
    tag = edge_cases(tag)
    # Finally, capitalize the first word regardless
    tag = tag[0].upper() + tag[1:]
    return tag


def edge_cases(tag):
    """Handle edge cases such as roman numerals and parentheses."""
    # Roman numerals
    if any(word.strip(':').strip(')') in ROMAN_NUMS for word in tag.split()):
        for word in tag.split():
            if word.strip(':') in ROMAN_NUMS:
                tag = tag.replace(word, word.upper())
    # Parentheses, colons, ellipses
    matches = re_parens.findall(tag)
    for match in matches:
        tag = tag.replace(match, match.upper())
    # Underscores (title likely pulled from file name)
    while '_' in tag:
        c = input(f'What character should replace the _ in {tag}? ')
        tag = tag.replace('_', c, 1)
    return tag


def mod_individual(artist_path):
    """Modify a single artist's songs."""
    modified = 0
    for album in artist_path.iterdir():
        album_path = artist_path / album
        if album.is_file():
            album = make_unknown(album_path)
        if album.name != 'Unknown Album':
            print(album.name)
        for song in album_path.iterdir():
            if song.is_dir():
                continue
            print(' ', song.stem)
            changed = modify_song(song)
            modified += 1 if changed else 0
    return modified


def main(base):
    modified = 0
    for artist in base.iterdir():
        artist_path = base / artist
        print(artist.name)
        for album in artist_path.iterdir():
            album_path = artist_path / album
            if album.is_file():
                album = make_unknown(album_path)
            if album.name != 'Unknown Album':
                print(' ', album.name)
            for song in album_path.iterdir():
                if song.is_dir():
                    continue
                changed = modify_song(song)
                modified += 1 if changed else 0
    return modified


if __name__ == '__main__':
    # base = Path('/Users/tmcou/Music/iTunes/iTunes Media/Music - Copy')
    # modified = main(base)
    base = Path('/Users/t/Music/Bought/Dirt Poor Robins')
    modified = mod_individual(base)
    print(f'\nModified {modified} songs.')
