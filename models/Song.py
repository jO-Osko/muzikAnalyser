# -*- coding: utf-8 -*-

"""Song model"""
import csv
import string
from typing import List

from models.PrintableStructure import PrintableStructure

__author__ = "Filip Koprivec"


# Make canonical
class Canonizer:
    def __init__(self, allowed_chars=string.ascii_lowercase+string.digits, forbidden_words=("official", "video", "radio", "edit")):
        self.allowed_chars = set(allowed_chars)
        self.chars_replace_dict = {"č": "c", "š": "s", "ć": "c", "ž": "z", "đ": "dj", "ł": "l", "ß": "ss"}
        self.special_replace_dict = {"'": ""}  # For  "It's something" == "Its something"
        self.forbidden_words = set(forbidden_words)

    def is_allowed_char(self, char: str) -> bool:
        return char in self.allowed_chars

    def is_allowed_word(self, word: str) -> bool:
        return word not in self.forbidden_words

    def translate(self, name: str) -> str:
        name = [self.chars_replace_dict.get(c, c) for c in name]
        name = [self.special_replace_dict.get(c, c) for c in name]
        name = [c if self.is_allowed_char(c) else " " for c in name]
        return "".join(name)

    def canonize(self, name: str) -> str:
        name = self.translate(name.lower()).split()
        name = filter(lambda x: self.is_allowed_word(x), name)
        return " ".join(sorted(name))


class Song(PrintableStructure):
    __slots__ = ["muzik_id", "name", "server", "bit_rate", "duration", "size", "frequency", "canonic_name"]
    __printable_fields__ = __slots__

    __printable_name__ = "Song"

    cannonizer = Canonizer()
    analyzing_servers = {514, 442, 443, 590, 1152, 520, 516, 1157, 470, 453, 451, 471}

    def __init__(self, muzik_id, name, server, bit_rate, duration, size, frequency):
        self.muzik_id = muzik_id                                    # type: str
        self.name = name                                            # type: str
        self.server = int(server)                                   # type: int
        self.bit_rate = int(bit_rate) if bit_rate else 0            # type: int
        self.duration = int(duration) if duration else 0            # type: int
        self.size = int(size) if size else 0                        # type: int
        self.frequency = int(frequency) if frequency else 0         # type: int
        self.canonic_name = self.make_canonic_name()                # type: str

    # Canonize name for song name comparison
    def make_canonic_name(self):
        return self.cannonizer.canonize(self.name)

    def to_comparable_song(self) -> "ComparableSong":
        return ComparableSong(self)

    def has_analyzing_server(self):
        return self.server in self.analyzing_servers

    @staticmethod
    def list_all_songs(file_path="data/main.csv") -> List["ComparableSong"]:
        songs = []
        with open(file_path, encoding="utf8") as in_file:
            reader = csv.reader(in_file)
            for row in reader:
                # Database is corrupted
                try:
                    song = Song.get_from_csv_array(row).to_comparable_song()
                    if song.song.has_analyzing_server():
                        songs.append(Song.get_from_csv_array(row).to_comparable_song())
                except Exception as e:
                    print(e)
        return songs

    @classmethod
    def get_from_csv_array(cls, array):
        return cls(array[0], array[2], array[1], array[12], array[10], array[11], array[15])


class ComparableSong(PrintableStructure):
    __slots__ = ["song", "comparable_name", "hash"]
    __printable_fields__ = __slots__

    __printable_name__ = "ComparableSong"

    def __init__(self, song: Song):
        self.song = song
        self.comparable_name = song.canonic_name
        self.hash = hash(self.comparable_name)

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        # Can be simplified to one line, I know
        if isinstance(other, ComparableSong):
            return self.comparable_name == other.comparable_name
        return False
