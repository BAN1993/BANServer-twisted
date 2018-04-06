#encoding:utf-8

import sys
sys.path.append("../base")

import Base
import ProtocolSRS
from CryptManager import gCrypt
import ConnectorClient

class client:

    m_conn = None

    def __init__(self,host,port):
        self.m_conn = ConnectorClient.ConnectorClient(self, host, port)
        self.m_conn.setReconnect(False)

    def run(self):
        self.m_conn.connect()
        from twisted.internet import reactor
        reactor.run()

    def recvFromServer(self,conn, data):
        ret, xyid, packlen, buf = Base.getXYHand(data)
        if xyid == ProtocolSRS.XYID_SRS_RESP_CONNECT:
            # print Base.getBytes(buf)
            resp = ProtocolSRS.RespConnect()
            resp.make(buf[0:packlen])
            print "connid=%d" % (resp.connid)

            req = ProtocolSRS.ReqLogin()
            req.connid = resp.connid
            req.numid = 1
            req.userid = "test3003"
            req.password = "123456"
            sendbuf = req.pack()
            self.m_conn.sendData(sendbuf)
        elif xyid == ProtocolSRS.XYID_SRS_RESP_LOGIN:
            resp = ProtocolSRS.RespLogin()
            resp.make(buf[0:packlen])
            print "flag=%d,numid=%d" % (resp.flag,resp.numid)

if __name__ == '__main__':
    gCrypt.setAESKey("SocketRouterSvr")

    c = client("127.0.0.1",8300)
    c.run()
