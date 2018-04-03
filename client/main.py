#encoding:utf-8

import sys
from twisted.internet.protocol import ClientFactory, Protocol
sys.path.append("../base")

import Base
import ProtocolSRS
from CryptManager import gCrypt
import ConnectorClient

class client:

    m_conn = None

    def __init__(self,host,port):
        self.m_conn = ConnectorClient.ConnectorClient(self, host, port)
    def run(self):
        self.m_conn.connect()

        from twisted.internet import reactor
        reactor.run()

    def recvFromServer(self,conn,data):
        ret, xyid, packlen, buf = Base.getXYHand(data)
        if xyid == ProtocolSRS.XYID_SRS_RESP_CONNECT:
            # print Base.getBytes(buf)
            resp = ProtocolSRS.RespConnect()
            resp.make(buf[0:packlen])
            print "connid=%d" % (resp.connid)

            req = ProtocolSRS.ReqLogin()
            req.numid = 1
            req.userid = "test3001"
            req.password = "123456"
            sendbuf = req.pack()
            self.m_conn.sendData(sendbuf)

if __name__ == '__main__':
    gCrypt.setAESKey("SocketRouterSvr")

    c = client("127.0.0.1",8300)
    c.run()
