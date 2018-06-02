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

    __isAuth = False

    def __init__(self,manager,conn):
        self.m_playerManager = manager
        self.m_conn = conn
        self.m_ip = conn.transport.hostname

    def recvData(self,conn,packlen,appid,numid,xyid,data):
        self.selectProtocol(conn,packlen,appid,numid,xyid,data)

    def sendData(self,data):
        self.m_conn.sendData(data)

    def setPlayerData(self,numid):
        self.m_numid = numid
        self.m_conn.m_numid = numid

    def selectProtocol(self,conn,packlen,appid,numid,xyid,data):
        logging.debug("packlen=%d,appid=%d,numid=%d,xyid=%d" % (packlen,appid,numid,xyid))
        protocol = Base.protocolBase()
        sendbuf = protocol.packUnknown(appid,numid,xyid,data)
        self.m_playerManager.m_server.sendToServer(sendbuf)

