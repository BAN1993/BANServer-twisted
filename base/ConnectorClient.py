#encoding:utf-8

import logging
from twisted.internet.protocol import ClientFactory, Protocol

"""
    连接客户端
    1.每个对象一个连接
    2.可设置是否自动重连
"""

class ConnectClientProtocl(Protocol):

    def connectionMade(self):
        self.factory.m_client.connectSuccess(self)
        self.factory.m_client.m_server.newServer(self.m_appid,self)

    def dataReceived(self, data):
        self.factory.m_client.m_server.recvFromServer(self.m_appid,self, data)

    def connectionLost(self, reason):
        logging.error("lost svr,reason=%s" % str(reason))
        self.factory.m_client.m_server.lostServer(self.m_appid,self)

class ConnectClientFactory(ClientFactory):

    protocol = ConnectClientProtocl

    m_client = None

    def __init__(self,client):
        self.m_client = client

    def clientConnectionFailed(self, connector, reason):
        logging.error("can not connect or lost,connector=%s.reason=%s" % (str(connector),str(reason)))
        self.m_client.m_server.lostServer(self)
        #self.reConnect()

    def reConnect(self):
        self.m_client.reConnect()

class ConnectorClient(object):

    m_conectFlag = False

    m_reconnect = True
    m_appid = 0
    m_host = ""
    m_port = 0

    m_server = None
    m_connector = None
    m_factory = None

    m_conn = None

    def __init__(self,server):
        self.m_server = server
        self.m_factory = ConnectClientFactory(self)

    def connect(self,appid,host,port):
        self.m_appid = appid
        self.m_host = host
        self.m_port = port
        logging.info("connect to ip=%s,post=%d" % (self.m_host, self.m_port))
        from twisted.internet import reactor
        self.m_connector = reactor.connectTCP(self.m_host, self.m_port, self.m_factory)

    def reConnect(self):
        if self.m_reconnect:
            from twisted.internet import reactor
            reactor.callLater(1,self.connect,self.m_host,self.m_port)

    def connectSuccess(self,conn):
        logging.info("connect success")
        self.m_conn = conn
        self.m_server.connectSuccess(self.m_appid,self)

    def sendData(self,data):
        #self.m_connector.write(data)
        if self.m_conn:
            self.m_conn.transport.write(data)
        else:
            logging.error("server conn is none")

    def setReconnect(self,setbool):
        self.m_reconnect = setbool
