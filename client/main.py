#encoding:utf-8

import sys
sys.path.append("../base")

import Base
import ServerInterface
import ProtocolSRS
from CryptManager import gCrypt
import ClientManager

class client(ServerInterface.ClientManager):

    m_host = ""
    m_port = 0

    m_conn = None

    def __init__(self,host,port):
        self.m_host = host
        self.m_port = port
        self.m_conn = ClientManager.ClientManager(self)

    def run(self):
        self.m_conn.addConnect(0,self.m_host,self.m_port)
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
            req.userid = "test3003"
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
    gCrypt.setAESKey("SocketRouterSvr")

    c = client("127.0.0.1",8300)
    c.run()
