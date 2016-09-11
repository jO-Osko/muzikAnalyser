# -*- coding: utf-8 -*-

"""Song model"""
import string

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
        return " ".join(name)


class Song:
    __slots__ = ["muzik_id", "name", "server", "bit_rate", "duration", "size", "frequency", "canonic_name"]

    cannonizer = Canonizer()

    def __init__(self, muzik_id, name, server, bit_rate, duration, size, frequency):
        self.muzik_id = muzik_id                        # type: str
        self.name = name                                # type: str
        self.server = server                            # type: str
        self.bit_rate = bit_rate                        # type: int
        self.duration = duration                        # type: int
        self.size = size                                # type: int
        self.frequency = frequency                      # type: int
        self.canonic_name = self.make_canonic_name()    # type: str

    # Canonize name for song name comparison
    def make_canonic_name(self):
        return self.cannonizer.canonize(self.name)


class ComparableSong:
    __slots__ = ["song", "comparable_name", "hash"]

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
