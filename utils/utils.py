# -*- coding: utf-8 -*-

"""Utils"""
import csv
import hashlib

__author__ = "Filip Koprivec"

import sqlite3
import os.path


class Utils:

    base_servers = {442: "balkanmp3_new", 443: "balkanmp3s_old", 451: "yucafe_old", 453: "yucafe_new",
                        470: "narodnjak.si", 471: "zlatizvoki.com", 514: "balkandj", 516: "mixoteka", 520: "megamixers",
                        590: "folkoteka", 1152: "klav.ma3x.org", 1157: "muzickinet"}

    def __init__(self, servers=None):
        self.servers = servers if servers else self.base_servers

        self.server_ids = [j for j in self.servers]

    def export_database(self):
        if not os.path.exists(os.path.join("data", "sqlite.db")):
            raise FileNotFoundError()
        base_conn = sqlite3.connect(os.path.join("data", "sqlite.db"))
        base_conn.text_factory = lambda x: str(x, "utf8", "ignore")
        cursor = base_conn.cursor()

        cursor.execute("SELECT id, name, server, bitr, time, size, freq FROM main")
        with open(os.path.join("data", "export.csv"), "w", encoding="utf8", newline="") as out_csv:
            csv_writer = csv.writer(out_csv, quoting=csv.QUOTE_MINIMAL)
            for result in cursor:
                csv_writer.writerow(list(result))

        # Export for validation
        cursor.execute("SELECT id, name, server, bitr, time, size, freq FROM main "
                        # I know this is bad, but normal parametrized queries do not work
                       "WHERE server IN {servers}".format(servers=tuple(self.get_server_ids())))

        with open(os.path.join("data", "export_servers.csv"), "w", encoding="utf8", newline="") as out_csv:
            csv_writer = csv.writer(out_csv, quoting=csv.QUOTE_MINIMAL)
            for result in cursor:
                csv_writer.writerow(list(result))

        print("Exported database")

        self.calculate_hash_of_non_versioned_files()

        print("Hashed files")

    # Calculate hash of non versioned files, to ensure, that i did not cheat with data
    def calculate_hash_of_non_versioned_files(self):
        filenames = ["export.csv", "export_servers.csv", "main.csv", "sqlite.db"]

        files = [(os.path.join("data", filename), os.path.join("data", filename + ".hash")) for filename in filenames]

        for in_file_path, out_file_path in files:
            open(out_file_path, "w").write(str(self.hash_file(in_file_path)))

    def hash_file(self, file_path, hash_algorithm=hashlib.sha512(), buff=65536):
        in_file = open(file_path, "rb")
        buf = in_file.read(buff)
        while len(buf):
            hash_algorithm.update(buf)
            buf = in_file.read(buff)

        return hash_algorithm.hexdigest()

    def get_server_ids(self):
        return self.server_ids

    def get_server_dict(self):
        return self.servers
