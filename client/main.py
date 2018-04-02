#encoding:utf-8

import socket
import sys
from twisted.internet.protocol import ClientFactory, Protocol
sys.path.append("../SocketRouterServer/logic")

import Base
import ProtocolSRS
from CryptManager import gCrypt

class ConnectClientProtocl(Protocol):

    def dataReceived(self, data):
        ret, xyid, packlen, buf = Base.getXYHand(data)
        if xyid == ProtocolSRS.XYID_SRS_RESP_CONNECT:
            #print Base.getBytes(buf)
            resp = ProtocolSRS.RespConnect()
            resp.make(buf[0:packlen])
            print "connid=%d" % (resp.connid)

            req = ProtocolSRS.ReqLogin()
            req.numid = 1
            req.userid = "test3001"
            req.password = "123456"
            sendbuf = req.pack()
            self.transport.write(sendbuf)


    def connectionLost(self, reason):
        print("lost gameserver,reason=",reason)

class ConnectClientFactory(ClientFactory):

    protocol = ConnectClientProtocl

    def clientConnectionFailed(self, connector, reason):
        print("can not connect,connector=%s.reason=%s" % (str(connector),str(reason)))

if __name__ == '__main__':
    gCrypt.setAESKey("SocketRouterSvr")

    factory = ConnectClientFactory()
    from twisted.internet import reactor

    reactor.connectTCP("127.0.0.1", 8300, factory)
    reactor.run()
