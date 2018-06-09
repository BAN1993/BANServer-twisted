#encoding:utf-8

from twisted.internet.protocol import ServerFactory, Protocol
import logging
import struct
import time

import Base
import ProtocolBS
import CryptManager

"""
    连接服务端
"""

class ConnectServerProtocl(Protocol):

    m_isAuth = False
    m_buf = ""
    m_connid = 0
    m_numid = 0 # 对服务来说,这里其实是appid
    m_crypt = None
    m_svrtype = 0 # 连接来的是服务才有效

    def connectionMade(self):
        self.m_isAuth = False
        self.m_buf = ""
        self.m_crypt = CryptManager.CryptManager()
        self.m_crypt.setAESKey("BansvrDFKey2018")
        #不通知上层,先验证连接
        #self.factory.m_server.newClient(self)

    def dataReceived(self, data):
        self.m_buf += data
        self.parseBuf()

    def connectionLost(self, reason):
        self.m_buf = ""
        self.factory.m_server.loseClient(self)

    def parseBuf(self):
        while True:
            packlen = Base.getPackLen(self.m_buf)
            if packlen <= 0:
                return
            if packlen + Base.LEN_SHORT > len(self.m_buf):
                return
            src = self.m_buf[0: packlen + Base.LEN_SHORT]
            self.m_buf = self.m_buf[packlen + Base.LEN_SHORT:]

            #解密
            (alllen,) = struct.unpack("H", src[0 : Base.LEN_SHORT] )
            xyDataSrc = src[Base.LEN_SHORT : alllen + Base.LEN_SHORT]
            buf = self.m_crypt.decryptAES(xyDataSrc)

            ret, packlen, appid, numid, xyid, data = Base.getXYHand(buf)
            if ret:
                if xyid == ProtocolBS.XYID_REQ_AUTH:
                    mpc = ProtocolBS.ReqAuth()
                    mpc.make(data)
                    self.m_numid = mpc.appid
                    self.m_svrtype = mpc.svrtype
                    key = "%d%d%d" % (self.m_numid,self.m_svrtype,int(time.time()))
                    logging.info("new auth:appid=%d,svrtype=%d" % (self.m_numid,self.m_svrtype))

                    resp = ProtocolBS.RespAuth()
                    resp.key = key
                    buf = resp.pack()
                    self.sendData(buf)

                    #发送key后开始使用新的key
                    self.m_crypt.setAESKey(key)
                    self.factory.m_server.newClient(self)
                else:
                    self.factory.m_server.recvFromClient(self, packlen, appid, numid, xyid, data)
            else:
                logging.error("parseBuf error")

    def sendData(self,data):
        cryptBuf = self.m_crypt.encryptAES(data)
        buflen = len(cryptBuf)
        lenbytes = struct.pack("H", buflen)
        cryptBuf = lenbytes[0: 2] + cryptBuf
        self.transport.write(cryptBuf)

class ConnectServerFactory(ServerFactory):

    protocol = ConnectServerProtocl

    m_server = None

    def __init__(self,server):
        self.m_server = server

class ConnectorServer(object):

    m_port = 0
    m_factory = None

    def __init__(self,server):
        self.m_factory = ConnectServerFactory(server)

    def begin(self,port):
        self.m_port = port
        logging.info("begin listen:%d" % self.m_port)
        from twisted.internet import reactor
        reactor.listenTCP(self.m_port, self.m_factory)
