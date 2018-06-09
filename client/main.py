#encoding:utf-8

import sys
sys.path.append("../base")

import Base
import log
import ServerInterface
import ProtocolSRS
import ClientManager

class client(ServerInterface.ClientManager):

    m_conn = None

    def __init__(self):
        self.m_conn = ClientManager.ClientManager(self)

    def run(self):
        self.m_conn.addConnect(1, "127.0.0.1", 8302)
        from twisted.internet import reactor
        reactor.run()

    def recvData(self,packlen,appid,srcappid,numid,xyid,data):
        if xyid == ProtocolSRS.XYID_SRS_RESP_CONNECT:
            # print Base.getBytes(buf)
            resp = ProtocolSRS.RespConnect()
            resp.make(data)
            print "connid=%d" % (resp.connid)

            req = ProtocolSRS.ReqLogin()
            req.connid = resp.connid
            req.userid = "test0001"
            req.password = "123456"
            sendbuf = req.pack()
            print "send login:userid=%s" % (req.userid)
            self.m_conn.sendData(sendbuf)
        elif xyid == ProtocolSRS.XYID_SRS_RESP_LOGIN:
            resp = ProtocolSRS.RespLogin()
            resp.make(data)
            print "recv respLogin:flag=%d,numid=%d" % (resp.flag,resp.numid)
            if resp.flag != resp.FLAG.SUCCESS:
                from twisted.internet import reactor
                reactor.stop()

if __name__ == '__main__':
    log.initLog("client", 0)

    c = client()
    c.run()
