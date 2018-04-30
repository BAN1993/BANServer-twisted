#encoding:utf-8

import logging
from twisted.internet.protocol import ClientFactory, Protocol

class ConnectClientProtocl(Protocol):

    def connectionMade(self):
        self.factory.m_client.setConn(self)
        self.factory.m_client.m_server.newServer(self)

    def dataReceived(self, data):
        self.factory.m_client.m_server.recvFromServer(self, data)

    def connectionLost(self, reason):
        logging.error("lost svr,reason=%s" % str(reason))
        #重连应该由上层管理
        #self.factory.reConnect()
        self.factory.m_client.m_server.lostServer(self)

class ConnectClientFactory(ClientFactory):

    protocol = ConnectClientProtocl

    m_client = None

    def __init__(self,client):
        self.m_client = client

    def clientConnectionFailed(self, connector, reason):
        logging.error("can not connect,connector=%s.reason=%s" % (str(connector),str(reason)))
        self.reConnect()

    def reConnect(self):
        self.m_client.reConnect()

class ConnectorClient(object):

    m_conectFlag = False

    m_reconnect = True
    m_host = ""
    m_port = 0

    m_server = None
    m_connector = None
    m_factory = None

    m_conn = None

    def __init__(self,server):
        self.m_server = server
        self.m_factory = ConnectClientFactory(self)

    def connect(self,host,port):
        self.m_host = host
        self.m_port = port
        logging.info("connect to ip=%s,post=%d" % (self.m_host, self.m_port))
        from twisted.internet import reactor
        self.m_connector = reactor.connectTCP(self.m_host, self.m_port, self.m_factory)

    def reConnect(self):
        if self.m_reconnect:
            from twisted.internet import reactor
            reactor.callLater(1,self.connect,self.m_host,self.m_port)

    def setConn(self,conn):
        logging.info("set conn")
        self.m_conn = conn

    def sendData(self,data):
        #self.m_connector.write(data)
        if self.m_conn:
            self.m_conn.transport.write(data)
        else:
            logging.error("server conn is none")

    def setReconnect(self,setbool):
        self.m_reconnect = setbool
