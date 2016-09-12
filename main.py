# -*- coding: utf-8 -*-

"""Muzik analyser"""
from collections import defaultdict
import pickle
import os.path

from models.Song import Song
from utils.utils import Utils

__author__ = "Filip Koprivec"


def main():

    utils = Utils()

    utils.export_database()

    print("Importing songs...")

    songs = Song.list_all_songs_from_analyzing_servers()

    print("All songs:", len(songs))

    similar = defaultdict(list)

    for song in songs:
        similar[song.comparable_name].append(song)

    duplicates = []
    for name, duplicate_songs in similar.items():
        if len(duplicate_songs) > 2:
            duplicates.append(duplicate_songs)

    pickle.dump(songs, open(os.path.join("data", "output", "songs.out"), "wb"))
    pickle.dump(duplicates, open(os.path.join("data", "output", "duplicates.out"), "wb"))
    print("Duplicates:", len(duplicates))


if __name__ == '__main__':
    main()
