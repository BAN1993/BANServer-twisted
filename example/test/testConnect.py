import sys
sys.path.append("../../base")

import ConnectorClient

class testServer:
    m_con1 = None
    m_con2 = None
    m_ret1 = None
    m_ret2 = None
    def __init__(self):
        print("begin try 1")
        self.m_con1 = ConnectorClient.ConnectorClient(self, "127.0.0.1", 8300)
        self.m_con2 = ConnectorClient.ConnectorClient(self, "127.0.0.1", 8301)
        self.m_con1.connect()
        from twisted.internet import reactor
        reactor.run()

    def recvFromServer(self,conn,data):
        pass

    def newServer(self,conn):
        if not self.m_ret1:
            print "set ret1=conn"
            self.m_ret1 = conn
            self.m_con2.connect()
        else:
            if not self.m_ret2:
                print "set ret2=conn"
                self.m_ret2 = conn
            else:
                print "all setted"


if __name__ == '__main__':
    svr = testServer()