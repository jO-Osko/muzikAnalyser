# -*- coding: utf-8 -*-

"""Simple PrintableStructure interface"""

__author__ = "Filip Koprivec"


class PrintableStructure:
    # Object methods
    __printable_fields__ = []
    __printable_name__ = "PrintableStructure"
    _formatter = "{name}({data})"

    def _str_fields(self):
        return ", ".join(map(repr, map(lambda x: self.__getattribute__(x), self.__printable_fields__)))

    def __repr__(self):
        return self._formatter.format(name=self.__printable_name__, data=self._str_fields())

    # For convenience
    def __str__(self):
        return self.__repr__()
