
import logging
from twisted.internet.protocol import ServerFactory, Protocol

class ConnectServerProtocl(Protocol):

    m_connid = 0
    m_numid = 0

    def connectionMade(self):
        self.factory.m_server.newClient(self)

    def dataReceived(self, data):
        self.factory.m_server.recvFromClient(self,data)

    def connectionLost(self, reason):
        self.factory.m_server.loseClient(self)

class ConnectServerFactory(ServerFactory):

    protocol = ConnectServerProtocl

    m_server = None

    def __init__(self,server):
        self.m_server = server

class ConnectorServer(object):

    m_port = 0
    m_factory = None

    def __init__(self,server,port):
        self.m_port = port
        self.m_factory = ConnectServerFactory(server)

    def begin(self):
        logging.info("begin listen:%d" % self.m_port)
        from twisted.internet import reactor
        reactor.listenTCP(self.m_port, self.m_factory)
