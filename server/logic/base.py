#encoding:utf-8

import time
import struct
import logging

from cryptManager import gCrypt

LEN_INT = 4

class protocolException(RuntimeError):
    def __init__(self, arg):
        self.msg = arg

class cryptException(RuntimeError):
    def __init__(self, arg):
        self.msg = arg

class protocolBase(object):
    bs_nowindex = 0
    bs_buf = ""

    def __init__(self):
        self.bs_nowindex = 0
        self.bs_buf = ""

    # Make
    #------------------------------------------------------------------------------------------------------------------------
    def makeBegin(self, buf):
        self.bs_nowindex = 0
        self.bs_buf = buf

    def getInt(self):
        if len(self.bs_buf) < self.bs_nowindex + LEN_INT:
            raise protocolException("data len err,datalen=" + str(len(self.bs_buf)) + ",aimlen=" + str(self.bs_nowindex + LEN_INT))
        (ret,) = struct.unpack('i', self.bs_buf[self.bs_nowindex : self.bs_nowindex + LEN_INT])
        self.bs_nowindex += LEN_INT
        return ret

    def getStr(self):
        strlen = self.getInt()
        if len(self.bs_buf) < self.bs_nowindex + strlen:
            raise protocolException("data len err,datalen=" + str(len(self.bs_buf)) + ",aimlen=" + str(self.bs_nowindex + strlen))
        (ret,) = struct.unpack(str(strlen) + "s", self.bs_buf[self.bs_nowindex : self.bs_nowindex + strlen])
        self.bs_nowindex += strlen
        return ret

    # Pack
    # ------------------------------------------------------------------------------------------------------------------------
    def replaceHand(self):
        strlen = len(self.bs_buf)
        lenbuf = struct.pack("i",strlen)
        for i in range(4,8):
            self.bs_buf = self.bs_buf[:i] + lenbuf[i-4] + self.bs_buf[(i+1):]

    def packBegin(self,xyid):
        self.bs_nowindex = 0
        self.bs_buf = struct.pack("ii", xyid, 0)

    def packInt(self,num):
        self.bs_buf = self.bs_buf + struct.pack("i", num)

    def packStr(self,src):
        strlen = len(src)
        self.bs_buf = self.bs_buf + struct.pack("i" + str(strlen) + "s", strlen, src)

    def packEnd(self):
        self.replaceHand()
        cryptBuf = gCrypt.encryptAES(self.bs_buf)
        buflen = len(cryptBuf)
        lenbytes = struct.pack("i", buflen)
        cryptBuf = lenbytes[0 : 4] + cryptBuf
        return cryptBuf

def getEnum(**enums):
    return type('Enum', (), enums)

def getBytes(data):
    return ' '.join(['0x%x' % ord(x) for x in data])

def getBytesIndex(data, begin, strlen):
    if len(data) < begin + strlen:
        logging.error("data len<" + str(begin + strlen))
        return ""
    return ' '.join(['0x%x' % ord(data[x]) for x in range(begin, begin + strlen)])

def getXYHand(data):
    if len(data)<LEN_INT:
        return False, 0, 0, ""
    (alllen,) = struct.unpack("i", data[0 : LEN_INT] )
    if len(data) < alllen + LEN_INT:
        return False, 0, 0, ""
    xyDataSrc = data[LEN_INT : alllen + LEN_INT]
    xyData = gCrypt.decryptAES(xyDataSrc)
    if len(xyData) < LEN_INT * 2:
        return False, 0, 0, ""
    (xyid, packlen, ) = struct.unpack('ii', xyData[0 : LEN_INT * 2])
    if xyid <= 0 or packlen <= 0:
        return False, xyid, packlen, ""
    return True,xyid,packlen,xyData

def getPackLen(data):
    if len(data) < LEN_INT:
        return 0
    (packlen, ) = struct.unpack("i", data[0 : LEN_INT])
    return packlen

def getMSTime():
    now = time.time()
    return int(round(now * 1000))

