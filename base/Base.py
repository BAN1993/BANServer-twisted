#encoding:utf-8

import time
import struct
import logging

"""
# Protocol Hand
# buflen    2   H   unsigned short
# appid     2   H   unsigned short
# numid     4   I   unsigned int
# xyid      4   I   unsigned int
"""

from CryptManager import gCrypt

LEN_HAND = 12
LEN_SHORT = 2
LEN_INT = 4

XYID_SRS_BEGIN  = 10001
XYID_SRS_END    = 20000
XYID_GAME_BEGIN = 20001
XYID_GAME_END   = 20001

class protocolException(RuntimeError):
    def __init__(self, arg):
        self.msg = arg

class cryptException(RuntimeError):
    def __init__(self, arg):
        self.msg = arg

class dbException(RuntimeError):
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
        lenbuf = struct.pack("H",strlen)
        for i in range(3,4):
            self.bs_buf = self.bs_buf[:i] + lenbuf[i-3] + self.bs_buf[(i+1):]

    def setHand(self,appid=0,numid=0):
        setbuf = struct.pack("HI",appid,numid)
        for i in range(5,10):
            self.bs_buf = self.bs_buf[:i] + setbuf[i-5] + self.bs_buf[(i+1):]

    def packBegin(self,xyid):
        self.bs_nowindex = 0
        self.bs_buf = struct.pack("HHII", 0,0,0,xyid)

    def packInt(self,num):
        num = int(num)
        self.bs_buf = self.bs_buf + struct.pack("i", num)

    def packStr(self,src):
        src = str(src)
        strlen = len(src)
        self.bs_buf = self.bs_buf + struct.pack("i" + str(strlen) + "s", strlen, src)

    def packEnd(self):
        self.replaceHand()
        cryptBuf = gCrypt.encryptAES(self.bs_buf)
        buflen = len(cryptBuf)
        lenbytes = struct.pack("I", buflen)
        cryptBuf = lenbytes[0 : 2] + cryptBuf
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
    if len(data)<LEN_HAND:
        return False, 0, 0, 0, 0, ""
    (alllen,) = struct.unpack("I", data[0 : LEN_SHORT] )
    if len(data) < alllen + LEN_SHORT:
        return False, 0, 0, 0, 0, ""
    xyDataSrc = data[LEN_SHORT : alllen + LEN_SHORT]
    xyData = gCrypt.decryptAES(xyDataSrc)
    if len(xyData) < LEN_HAND:
        return False, 0, 0, 0, 0, ""
    (packlen, appid, numid, xyid, ) = struct.unpack('HHII', xyData[0 : LEN_HAND])
    if xyid <= 0 or packlen <= 0:
        return False, packlen, appid, numid, xyid, ""
    return True,packlen, appid, numid, xyid, xyData

def getPackLen(data):
    if len(data) < LEN_INT:
        return 0
    (packlen, ) = struct.unpack("I", data[0 : LEN_SHORT])
    return packlen

def getMSTime():
    now = time.time()
    return int(round(now * 1000))

