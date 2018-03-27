
class ConnectorClient(object):

    m_host = ""
    m_port = 0

    m_server = None

    def __init__(self,server,host,port):
        self.m_host = host
        self.m_port = port
        m_server = server

    def connect(self):
        from twisted.internet import reactor
        reactor.connectTCP(gIp, gPort, factory)
        reactor.run()
