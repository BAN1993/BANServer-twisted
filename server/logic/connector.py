
#from twisted.internet.protocol import Factory
from twisted.internet.protocol import ServerFactory, Protocol

class connectProtocl(Protocol):

    def connectionMade(self):
        self.factory.m_server.newConnect(self)

    def dataReceived(self, data):
        self.factory.m_server.recvData(self,data)

    def connectionLost(self, reason):
        self.factory.m_server.loseConnect(self)

class connectFactory(ServerFactory):

    protocol = connectProtocl

    m_server = None

    def __init__(self,server):
        self.m_server = server

class Connector(object):

    m_factory = None
    #m_server = None

    def __init__(self,server):
        #m_server = server
        m_factory = connectFactory(server)
        from twisted.internet import reactor
        port = reactor.listenTCP(server.m_port, m_factory)

    def run(self):
        from twisted.internet import reactor
        reactor.run()