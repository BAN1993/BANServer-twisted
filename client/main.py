#encoding:utf-8

import sys
sys.path.append("../base")

import Base
import ProtocolSRS
from CryptManager import gCrypt
import ConnectorClient

class client:

    m_conn = None
    __recvBuf = ""

    def __init__(self,host,port):
        self.m_conn = ConnectorClient.ConnectorClient(self, host, port)
        self.m_conn.setReconnect(False)

    def run(self):
        self.m_conn.connect()
        from twisted.internet import reactor
        reactor.run()

    def newServer(self,conn):
        print "new server"

    def recvFromServer(self,conn, data):
        self.__recvBuf += data
        while True:
            packlen = Base.getPackLen(self.__recvBuf)
            if packlen <= 0:
                return
            if packlen + Base.LEN_SHORT > len(self.__recvBuf):
                return
            data = self.__recvBuf[0: packlen + Base.LEN_SHORT]
            self.__recvBuf = self.__recvBuf[packlen + Base.LEN_SHORT:]
            ret, packlen, appid, numid, xyid, buf = Base.getXYHand(data)
            if not ret:
                print("getXYHand error")
                continue
            print("packlen=%d,appid=%d,numid=%d,xyid=%d" % (packlen,appid,numid,xyid))
            if xyid == ProtocolSRS.XYID_SRS_RESP_CONNECT:
                # print Base.getBytes(buf)
                resp = ProtocolSRS.RespConnect()
                resp.make(buf)
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
                resp.make(buf)
                print "recv respLogin:flag=%d,numid=%d" % (resp.flag,resp.numid)
                if resp.flag != resp.FLAG.SUCCESS:
                    from twisted.internet import reactor
                    reactor.stop()

if __name__ == '__main__':
    gCrypt.setAESKey("SocketRouterSvr")

    c = client("127.0.0.1",8300)
    c.run()
