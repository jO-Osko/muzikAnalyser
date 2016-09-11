# -*- coding: utf-8 -*-

"""Utils"""
import csv

__author__ = "Filip Koprivec"

import sqlite3
import os.path


class Utils:
    def __init__(self):
        pass

    def export_database(self, servers=(514, 442, 443, 590, 1152, 520, 516, 1157, 470, 453, 451, 471)):
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
                       "WHERE server IN {servers}".format(servers=servers))

        with open(os.path.join("data", "export_servers.csv"), "w", encoding="utf8", newline="") as out_csv:
            csv_writer = csv.writer(out_csv, quoting=csv.QUOTE_MINIMAL)
            for result in cursor:
                csv_writer.writerow(list(result))
