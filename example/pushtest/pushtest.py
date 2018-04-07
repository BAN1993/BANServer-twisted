#encoding:utf-8

import sys
sys.path.append("../../base")

import Base
import ProtocolSRS
from CryptManager import gCrypt
import ConnectorClient

class client:

    m_conn = None
    __recvBuf = ""

    m_lastTime = 0
    m_recvTime = 0
    m_userid = ""
    m_numid = 0
    m_times = 0
    m_now = 0

    def __init__(self,host,port,userid,times):
        self.m_conn = ConnectorClient.ConnectorClient(self, host, port)
        self.m_conn.setReconnect(False)
        self.m_userid = userid
        self.m_times = times
        self.m_now = 0

    def run(self):
        self.m_conn.connect()
        from twisted.internet import reactor
        reactor.run()

    def newServer(self,conn):
        print "new server"

    def recvFromServer(self,conn, data):
        self.m_recvTime = Base.getMSTime()
        self.__recvBuf += data
        packlen = Base.getPackLen(self.__recvBuf)
        if packlen <= 0:
            return
        if packlen + Base.LEN_INT > len(self.__recvBuf):
            return
        data = self.__recvBuf[0: packlen + Base.LEN_INT]
        self.__recvBuf = self.__recvBuf[packlen + Base.LEN_INT:]
        ret, xyid, packlen, buf = Base.getXYHand(data)
        if xyid == ProtocolSRS.XYID_SRS_RESP_CONNECT:
            # print Base.getBytes(buf)
            resp = ProtocolSRS.RespConnect()
            resp.make(buf[0:packlen])
            print "connid=%d" % (resp.connid)

            req = ProtocolSRS.ReqLogin()
            req.connid = resp.connid
            req.numid = 0
            req.userid = self.m_userid
            req.password = "123456"
            sendbuf = req.pack()
            self.m_lastTime = Base.getMSTime()
            self.m_conn.sendData(sendbuf)
        elif xyid == ProtocolSRS.XYID_SRS_RESP_LOGIN:
            resp = ProtocolSRS.RespLogin()
            resp.make(buf[0:packlen])
            print "flag=%d,numid=%d" % (resp.flag,resp.numid)
            if resp.flag != resp.FLAG.SUCCESS :
                from twisted.internet import reactor
                reactor.stop()
            self.m_numid = resp.numid
            self.testGold()
        elif xyid == ProtocolSRS.XYID_SRS_RESP_GOLD:
            self.m_recvTime = Base.getMSTime()
            resp = ProtocolSRS.RespGold()
            resp.make(buf[0:packlen])
            print "numid=%d,gold=%Ld,use=%d" % (resp.numid, resp.gold, self.m_recvTime-self.m_lastTime)
            self.testGold()
        else:
            print("unknown xy,xyid=%d" % xyid)
            from twisted.internet import reactor
            reactor.stop()

    def testGold(self):
        if self.m_now >= self.m_times:
            from twisted.internet import reactor
            reactor.stop()
            print "test end"
            return
        self.m_now += 1
        req = ProtocolSRS.ReqGold()
        req.numid = self.m_numid
        sendbuf = req.pack()
        self.m_conn.sendData(sendbuf)
        self.m_lastTime = Base.getMSTime()



if __name__ == '__main__':
    gCrypt.setAESKey("SocketRouterSvr")

    if len(sys.argv) != 3:
        print("args error")
        exit()

    userid = str(sys.argv[1])
    times = int(sys.argv[2])
    print("userid=%s,times=%d" % (userid,times))
    c = client("127.0.0.1",8300,userid,times)
    c.run()
