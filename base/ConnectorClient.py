#encoding:utf-8

from twisted.internet.protocol import ClientFactory, Protocol
import logging
import struct

import Base
import ProtocolBS
import CryptManager

"""
    连接客户端
    1.每个对象一个连接
    2.可设置是否自动重连
"""

class ConnectClientProtocl(Protocol):

    def connectionMade(self):
        self.factory.m_client.connectMade(self)

    def dataReceived(self, data):
        self.factory.m_client.recvData(self,data)

    def connectionLost(self, reason):
        logging.error("lost svr,reason=%s" % str(reason))
        self.factory.m_client.connectLost(self)

class ConnectClientFactory(ClientFactory):

    protocol = ConnectClientProtocl

    m_client = None

    def __init__(self,client):
        self.m_client = client

    def clientConnectionFailed(self, connector, reason):
        logging.error("can not connect or lost,connector=%s.reason=%s" % (str(connector),str(reason)))
        self.m_client.connectLost(self)
        #self.reConnect()

    def reConnect(self):
        self.m_client.reConnect()

class ConnectorClient(object):

    m_conectFlag = False

    m_reconnect = True
    m_appid = 0
    m_host = ""
    m_port = 0
    m_svrtype = 0

    m_server = None
    m_connector = None
    m_factory = None

    m_buf = ""
    m_conn = None

    m_crypt = None

    def __init__(self,server):
        self.m_server = server
        self.m_factory = ConnectClientFactory(self)
        self.m_crypt = CryptManager.CryptManager()
        self.m_buf = ""
        self.m_crypt.setAESKey("BansvrDFKey2018")

    def connect(self,appid,host,port):
        self.m_appid = appid
        self.m_host = host
        self.m_port = port
        logging.info("connect to ip=%s,post=%d" % (self.m_host, self.m_port))
        from twisted.internet import reactor
        self.m_connector = reactor.connectTCP(self.m_host, self.m_port, self.m_factory)

    def reConnect(self):
        if self.m_reconnect:
            from twisted.internet import reactor
            reactor.callLater(1,self.connect,self.m_appid,self.m_host,self.m_port)

    def connectMade(self,conn):
        """连接成功,开始验证"""
        self.m_buf = ""
        self.m_conn = conn

        req = ProtocolBS.ReqAuth()
        req.appid = self.m_appid
        req.svrtype = self.m_svrtype
        buf = req.pack()
        self.sendData(buf)


    def connectSuccess(self,flag):
        logging.debug("flag=%d" % flag)
        self.m_server.connectSuccess(self.m_appid,self,flag)

    def connectLost(self,conn):
        self.m_buf = ""
        self.m_server.connectLost(self.m_appid,self)

    def sendData(self,data):
        if self.m_conn:
            # 加密
            cryptBuf = self.m_crypt.encryptAES(data)
            buflen = len(cryptBuf)
            lenbytes = struct.pack("H", buflen)
            cryptBuf = lenbytes[0: 2] + cryptBuf
            self.m_conn.transport.write(cryptBuf)
        else:
            logging.error("server conn is none")

    def recvData(self,conn,data):
        self.m_buf += data
        self.parseBuf()

    def setReconnect(self,setbool):
        self.m_reconnect = setbool

    def parseBuf(self):
        while True:
            packlen = Base.getPackLen(self.m_buf)
            if packlen <= 0:
                return
            if packlen + Base.LEN_SHORT > len(self.m_buf):
                return
            src = self.m_buf[0: packlen + Base.LEN_SHORT]
            self.m_buf = self.m_buf[packlen + Base.LEN_SHORT:]

            # 解密
            (alllen,) = struct.unpack("H", src[0: Base.LEN_SHORT])
            xyDataSrc = src[Base.LEN_SHORT: alllen + Base.LEN_SHORT]
            buf = self.m_crypt.decryptAES(xyDataSrc)

            ret, packlen, appid, numid, xyid, data = Base.getXYHand(buf)
            logging.debug("packlen=%d,appid=%d,numid=%d,xyid=%d,datalen=%d" % (packlen,appid,numid,xyid,len(data)))
            if ret:
                if xyid == ProtocolBS.XYID_RESP_AUTH:
                    resp = ProtocolBS.RespAuth()
                    ret = resp.make(data)
                    if not ret:
                        logging.error("make RespAuth error,stop server")
                        self.connectSuccess(False)
                    else:
                        self.m_crypt.setAESKey(resp.key)
                        self.connectSuccess(True)
                else:
                    self.m_server.recvData(packlen, appid, self.m_appid, numid, xyid, data)
            else:
                logging.error("parseBuf error")
