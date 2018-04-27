#encoding:utf-8

import logging
import sys
sys.path.append("../base")

import Base
import ConnectorClient
import ProtocolCFG

class ConfigClent:

    m_isConnected = False
    m_isInited = False
    m_subType = 0
    m_svrType = 0
    m_cfgIp = ""
    m_cfgPort = 0

    m_server = None
    m_conn = None
    m_connectCallback = None

    __recvData = ""

    m_appid = 0
    m_config = ""

    def __init__(self,server,subtype,svrtype,cfgip,cfgport):
        self.m_server = server
        self.m_subType = subtype
        self.m_svrType = svrtype
        self.m_cfgIp = cfgip
        self.m_cfgPort = cfgport

    def connect(self,callback):
        """callback(bool flag)"""
        self.m_conn = ConnectorClient.ConnectorClient(self, self.m_cfgIp, self.m_cfgPort)
        self.m_connectCallback = callback

    def newServer(self, conn):
        logging.info("connect configsvr success")
        self.m_isConnected = True
        if not self.m_isInited:
            req = ProtocolCFG.ReqConnect()
            req.subtype = self.m_subType
            req.svrtype = self.m_svrType
            buf = req.pack()
            self.m_conn.sendData(buf)

    def lostServer(self,conn):
        logging.warn("lost configsvr and try connect")
        self.m_isConnected = False
        self.m_conn.reConnect()

    def recvFromServer(self,conn,data):
        self.__recvData += data
        while True:
            packlen = Base.getPackLen(self.__recvData)
            if packlen <= 0:
                return
            if packlen + Base.LEN_SHORT > len(self.__recvData):
                return

            data = self.__recvData[0: packlen + Base.LEN_SHORT]
            self.__recvData = self.__recvData[conn][packlen + Base.LEN_SHORT:]
            self.selectProtocol(data)

    def selectProtocol(self,buf):
        ret, packlen, appid, numid, xyid, data = Base.getXYHand(buf)
        if not ret:
            logging.warning("getXYHand error")
            return
        logging.debug("packlen=%d,appid=%d,numid=%d,xyid=%d" % (packlen, appid, numid, xyid))
        # 处理特殊逻辑用
        if xyid == ProtocolCFG.XYID_CFG_RESP_CONNECT:
            resp = ProtocolCFG.RespConnect()
            ret = resp.make(data)
            logging.info("flag=%d,appid=%d,config=%d" % (resp.flag,resp.appid,resp.config))
            callbackflag = True
            if resp.flag == resp.FLAG.SUCCESS:
                self.m_isInited = True
                self.m_appid = resp.appid
                self.m_config = resp.config
            else:
                logging.error("connect configsvr failed,flag=%d" % resp.flag)
                callbackflag = False
            self.m_connectCallback(callbackflag)