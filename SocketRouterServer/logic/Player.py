#encoding:utf-8

import logging
import sys
sys.path.append("../..")

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

    def selectProtocol(self,xyid,data):
        logging.debug("xyid=%d" % xyid)
        if xyid == ProtocolSRS.XYID_SRS_REQ_LOGIN :
            req = ProtocolSRS.ReqLogin()
            ret = req.make(data)
            logging.info("connid=%d,numid=%d,userid=%s,pwd=%s" % (req.connid,req.numid, req.userid, req.password))

            reqsvr = ProtocolGAME.ReqLogin()
            reqsvr.connid = req.connid
            reqsvr.numid = req.numid
            reqsvr.userid = req.userid
            reqsvr.password = req.password
            buf = reqsvr.pack()
            self.m_playerManager.m_server.sendToSvr(buf)
