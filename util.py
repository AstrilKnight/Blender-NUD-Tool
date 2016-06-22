import struct
import os
import numpy as np


def clearConsole():
    clear = lambda: os.system('cls')
    clear()


def readByte(file):
    return struct.unpack("B", file.read(1))[0]


def readu16be(file):
    return struct.unpack(">H", file.read(2))[0]


def readu16le(file):
    return struct.unpack("<H", file.read(2))[0]


def readu32be(file):
    return struct.unpack(">I", file.read(4))[0]


def readu32le(file):
    return struct.unpack("<I", file.read(4))[0]


def readfloatbe(file):
    return struct.unpack(">f", file.read(4))[0]


def readfloatle(file):
    return struct.unpack("<f", file.read(4))[0]


def readhalffloatbe(f):
    # pos = f.tell()
    raw = f.read(2)
    float16 = float(np.frombuffer(raw, dtype=np.float16))
    return float16


def readhalffloatle(f):
    # pos = f.tell()
    return struct.unpack("<H", f.read(2))[0]

def readString(f, term=b'\0'):
    result = ""
    tmpChar = f.read(1).decode("ASCII")
    while ord(tmpChar) != 0:
        result += tmpChar
        tmpChar = f.read(1).decode("ASCII")
    return result
