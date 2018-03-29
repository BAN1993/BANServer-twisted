#encoding:utf-8

import socket
import sys
sys.path.append("../SocketRouterServer/logic")

import Base
import SRSProtocol
from CryptManager import gCrypt

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8300))
    gCrypt.setAESKey("SocketRouterSvr")

    recvBuf = sock.recv(1024)
    print recvBuf
    #recvData = gCrypt.decryptAES(recvBuf)
    ret, xyid, packlen, buf = Base.getXYHand(recvBuf)
    print Base.getBytes(buf)
    resp = SRSProtocol.RespConnect()
    resp.make(buf[0:packlen])
    print "connid=%d" % (resp.connid)