import struct
import os

class Float16Compressor:
    def __init__(self):
        self.temp = 0

    def compress(self,float32):
        F16_EXPONENT_BITS = 0x1F
        F16_EXPONENT_SHIFT = 10
        F16_EXPONENT_BIAS = 15
        F16_MANTISSA_BITS = 0x3ff
        F16_MANTISSA_SHIFT =  (23 - F16_EXPONENT_SHIFT)
        F16_MAX_EXPONENT =  (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

        a = struct.pack('>f',float32)
        b = binascii.hexlify(a)

        f32 = int(b,16)
        f16 = 0
        sign = (f32 >> 16) & 0x8000
        exponent = ((f32 >> 23) & 0xff) - 127
        mantissa = f32 & 0x007fffff

        if exponent == 128:
            f16 = sign | F16_MAX_EXPONENT
            if mantissa:
                f16 |= (mantissa & F16_MANTISSA_BITS)
        elif exponent > 15:
            f16 = sign | F16_MAX_EXPONENT
        elif exponent > -15:
            exponent += F16_EXPONENT_BIAS
            mantissa >>= F16_MANTISSA_SHIFT
            f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
        else:
            f16 = sign
        return f16

    def decompress(self,float16):
        s = int((float16 >> 15) & 0x00000001)    # sign
        e = int((float16 >> 10) & 0x0000001f)    # exponent
        f = int(float16 & 0x000003ff)            # fraction

        if e == 0:
            if f == 0:
                return int(s << 31)
            else:
                while not (f & 0x00000400):
                    f = f << 1
                    e -= 1
                e += 1
                f &= ~0x00000400
                #print(s,e,f)
        elif e == 31:
            if f == 0:
                return int((s << 31) | 0x7f800000)
            else:
                return int((s << 31) | 0x7f800000 | (f << 13))

        e = e + (127 -15)
        f = f << 13
        return int((s << 31) | (e << 23) | f)


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
    fcomp = Float16Compressor()
    fcomp.Float16Co
    return float(np.frombuffer(f.read(2), dtype=np.float16))


def readhalffloatbe(f):
    etmp = f.read(2)
    etmp = bytes([etmp[1], etmp[0]])
    h = struct.unpack(">H",etmp)[0]
    fcomp = Float16Compressor()
    temp = fcomp.decompress(h)
    stri = struct.pack('I',temp)
    return struct.unpack('f',stri)[0]


def readhalffloatle(f):
    etmp = f.read(2)
    h = struct.unpack(">H",etmp)[0]
    fcomp = Float16Compressor()
    temp = fcomp.decompress(h)
    stri = struct.pack('I',temp)
    return struct.unpack('f',stri)[0]


def readString(f, term=b'\0'):
    result = ""
    tmpChar = f.read(1).decode("ASCII")
    while ord(tmpChar) != 0:
        result += tmpChar
        tmpChar = f.read(1).decode("ASCII")
    return result
