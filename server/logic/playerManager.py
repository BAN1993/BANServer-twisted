

class playerManager(object):

    m_playerList = {}
    m_server = None

    def __init__(self,server):
        self.m_server = server

    def newConnect(self,protocol):
        pass

    def recvData(self,protocol,data):
        pass

    def loseConnect(self,protocol):
        pass
