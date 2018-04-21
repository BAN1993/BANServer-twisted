#encoding:utf-8

import logging
import sys
sys.path.append("../base")

import Base
import ProtocolSRS


class Player:

    m_playerManager = None
    m_conn = None
    m_ip = ""
    m_numid = 0

    __recvBuf = ""
    __isAuth = False

    def __init__(self,manager,conn):
        self.m_playerManager = manager
        self.m_conn = conn
        self.m_ip = conn.transport.hostname

    def recvData(self,data):
        self.__recvBuf += data
        while True:
            packlen = Base.getPackLen(self.__recvBuf)
            if packlen <= 0:
                return
            if packlen + Base.LEN_SHORT > len(self.__recvBuf):
                return
            src = self.__recvBuf[0: packlen + Base.LEN_SHORT]
            self.__recvBuf = self.__recvBuf[packlen + Base.LEN_SHORT:]
            self.selectProtocol(src)

    def sendData(self,data):
        self.m_conn.transport.write(data)

    def setPlayerData(self,numid):
        self.m_numid = numid
        self.m_conn.m_numid = numid

    def selectProtocol(self,buf):
        ret, packlen, appid, numid, xyid, data = Base.getXYHand(buf)
        if not ret:
            logging.warning("getXYHand error")
            return
        logging.debug("packlen=%d,appid=%d,numid=%d,xyid=%d" % (packlen,appid,numid,xyid))
        protocol = Base.protocolBase()
        sendbuf = protocol.packUnknown(appid,self.m_numid,xyid,data)
        self.m_playerManager.m_server.sendToServer(sendbuf)

