#encoding:utf-8

import logging
import sys
sys.path.append("../base")

import Base
import ProtocolGAME
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
        packlen = Base.getPackLen(self.__recvBuf)
        if packlen <= 0:
            return
        if packlen + Base.LEN_INT > len(self.__recvBuf):
            return
        data = self.__recvBuf[0: packlen + Base.LEN_INT]
        self.__recvBuf = self.__recvBuf[packlen + Base.LEN_INT:]
        ret, xyid, packlen, buf = Base.getXYHand(data)
        if ret:
            self.selectProtocol(xyid, buf[0: packlen])

    def sendData(self,data):
        self.m_conn.transport.write(data)

    def setPlayerData(self,numid):
        self.m_numid = numid
        self.m_conn.m_numid = numid

    def selectProtocol(self,xyid,data):
        if xyid == ProtocolSRS.XYID_SRS_REQ_LOGIN :
            req = ProtocolSRS.ReqLogin()
            ret = req.make(data)
            logging.info("ReqLogin:connid=%d,numid=%d,userid=%s,pwd=%s" % (req.connid,req.numid, req.userid, req.password))

            reqsvr = ProtocolGAME.ReqLogin()
            reqsvr.connid = req.connid
            reqsvr.numid = req.numid
            reqsvr.userid = req.userid
            reqsvr.password = req.password
            buf = reqsvr.pack()
            self.m_playerManager.m_server.sendToServer(buf)

        elif xyid == ProtocolSRS.XYID_SRS_REQ_GOLD:
            req = ProtocolSRS.ReqGold()
            ret = req.make(data)
            logging.info("ReqGold:numid=%d" % req.numid)

            reqsvr = ProtocolGAME.ReqGold()
            reqsvr.numid = req.numid
            buf = reqsvr.pack()
            self.m_playerManager.m_server.sendToServer(buf)

        else:
            logging.warning("unknown xy,xyid=%d" % xyid)
