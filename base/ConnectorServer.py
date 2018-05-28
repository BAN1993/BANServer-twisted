#encoding:utf-8

import Base
import logging
from twisted.internet.protocol import ServerFactory, Protocol

"""
    连接服务端
"""

class ConnectServerProtocl(Protocol):

    m_buf = ""
    m_connid = 0
    m_numid = 0 # 对服务来说,这里其实是appid

    def connectionMade(self):
        self.m_buf = ""
        self.factory.m_server.newClient(self)

    def dataReceived(self, data):
        self.m_buf += data
        self.parseBuf()

    def connectionLost(self, reason):
        self.m_buf = ""
        self.factory.m_server.loseClient(self)

    def parseBuf(self):
        while True:
            packlen = Base.getPackLen(self.m_buf)
            if packlen <= 0:
                return
            if packlen + Base.LEN_SHORT > len(self.m_buf):
                return
            src = self.m_buf[0: packlen + Base.LEN_SHORT]
            self.m_buf = self.m_buf[packlen + Base.LEN_SHORT:]
            ret, packlen, appid, numid, xyid, data = Base.getXYHand(src)
            if ret:
                self.factory.m_server.recvFromClient(self, packlen, appid, numid, xyid, data)
            else:
                logging.error("parseBuf error")

class ConnectServerFactory(ServerFactory):

    protocol = ConnectServerProtocl

    m_server = None

    def __init__(self,server):
        self.m_server = server

class ConnectorServer(object):

    m_port = 0
    m_factory = None

    def __init__(self,server):
        self.m_factory = ConnectServerFactory(server)

    def begin(self,port):
        self.m_port = port
        logging.info("begin listen:%d" % self.m_port)
        from twisted.internet import reactor
        reactor.listenTCP(self.m_port, self.m_factory)
