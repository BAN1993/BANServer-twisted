
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet import reactor
import logging

class ConnectClientProtocl(Protocol):

    def dataReceived(self, data):
        self.factory.m_client.m_server.recvFromServer(self, data)

    def connectionLost(self, reason):
        logging.error("lost gameserver")
        self.factory.reConnect()

class ConnectClientFactory(ClientFactory):

    protocol = ConnectClientProtocl

    m_client = None

    def __init__(self,client):
        self.m_client = client

    def clientConnectionFailed(self, connector, reason):
        logging.error("can not connect")
        self.reConnect()

    def reConnect(self):
        self.m_client.reConnect()

class ConnectorClient(object):

    m_host = ""
    m_port = 0

    m_server = None
    m_connector = None
    m_factory = None

    def __init__(self,server,host,port):
        self.m_host = host
        self.m_port = port
        self.m_server = server
        self.m_factory = ConnectClientFactory(self)

    def connect(self):
        self.m_connector = reactor.connectTCP(self.m_host, self.m_port, self.m_factory)

    def reConnect(self):
        reactor.callLater(1,self.connect)