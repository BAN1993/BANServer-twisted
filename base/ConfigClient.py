#encoding:utf-8

import logging
import sys
sys.path.append("../base")

import Base
import ServerInterface
import ConnectorClient
import ProtocolCFG

"""
    配置服务的客户端
    1.连接失败则停止服务
    2.第一次尝试连接不成功则视为失败,其他情况都会重连
"""

class ConfigClent(ServerInterface.ClientBase):

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

    __askid = 0
    __reqCallback = {} # [askid]=callback
    __reqRetStr = {} # [askid]=[retstr]

    m_appid = 0
    m_port = 0
    m_config = ""

    def __init__(self,server,subtype,svrtype,cfgip,cfgport):
        self.m_server = server
        self.m_subType = subtype
        self.m_svrType = svrtype
        self.m_cfgIp = cfgip
        self.m_cfgPort = cfgport

    def connect(self,callback):
        """callback(bool flag)"""
        logging.info("begin connect configsvr,ip=%s,port=%d" % (self.m_cfgIp,self.m_cfgPort))
        self.m_conn = ConnectorClient.ConnectorClient(self)
        self.m_conn.connect(0,self.m_cfgIp, self.m_cfgPort)
        self.m_connectCallback = callback

    def getPort(self):
        return self.m_port

    def getAppid(self):
        return self.m_appid

    def getConfig(self):
        return self.m_config

    def GetConfigBySql(self,sqlstr,callback):
        """callback(bool flag, list [configstr])"""
        self.__askid += 1

        req = ProtocolCFG.ReqConfig()
        req.askid = self.__askid
        req.sqlstr = sqlstr
        buf = req.pack()
        self.m_conn.sendData(buf)

        self.__reqCallback[req.askid] = callback
        self.__reqRetStr[req.askid] = []

    def connectSuccess(self, appid,client,flag):
        if flag:
            logging.info("connect to configsvr success")
            self.m_isConnected = True
            if not self.m_isInited:
                req = ProtocolCFG.ReqConnect()
                req.subtype = self.m_subType
                req.svrtype = self.m_svrType
                buf = req.pack()
                self.m_conn.sendData(buf)
        else:
            logging.error("connect to configsvr failed")
            self.connectLost(appid,client)


    def connectLost(self,appid,client):
        if self.m_isInited:
            #如果已经验证过,则可以重连
            logging.warn("lost configsvr and try connect")
            self.m_isConnected = False
            self.noticeAllCallBackFail()
            self.m_conn.reConnect()
        else:
            #如果没验证过,直接停止服务
            logging.error("can not connect to configsvr and stop")
            self.m_server.stop()

    def noticeAllCallBackFail(self):
        """通知所有回调失败,并清理列表"""
        for cb in self.__reqCallback.values():
            cb(False,[])
        self.__reqCallback.clear()
        self.__reqRetStr.clear()
        self.__recvData = ""

    def recvData(self,packlen,appid,srcappid,numid,xyid,data):
        if not self.m_isConnected:
            logging.error("recv data but is not connnected")
            return
        self.selectProtocol(packlen,appid,srcappid,numid,xyid,data)

    def selectProtocol(self,packlen,appid,srcappid,numid,xyid,data):
        logging.debug("packlen=%d,appid=%d,srcappid=%d,numid=%d,xyid=%d" % (packlen, appid, srcappid, numid, xyid))

        if xyid == ProtocolCFG.XYID_CFG_RESP_CONNECT:
            resp = ProtocolCFG.RespConnect()
            ret = resp.make(data)
            logging.info("flag=%d,appid=%d,port=%d,config=%s" % (resp.flag,resp.appid,resp.port,resp.config))
            callbackflag = True
            if resp.flag == resp.FLAG.SUCCESS:
                self.m_isInited = True
                self.m_appid = resp.appid
                self.m_port = resp.port
                self.m_config = resp.config
            else:
                logging.error("connect configsvr failed,flag=%d" % resp.flag)
                callbackflag = False
            self.m_connectCallback(callbackflag)

        elif xyid == ProtocolCFG.XYID_CFG_RESP_CONFIG:
            resp = ProtocolCFG.RespConfig()
            ret = resp.make(data)
            logging.debug("askid=%d,retstr=%s" % (resp.askid,resp.retstr))
            self.__reqRetStr[resp.askid].append(resp.retstr)

        elif xyid == ProtocolCFG.XYID_CFG_RESP_CONFIGFINISH:
            resp = ProtocolCFG.RespConfigFinish()
            ret = resp.make(data)
            logging.debug("askid=%d,flag=%d,count=%d" % (resp.askid,resp.flag,resp.count))
            if resp.flag == resp.FLAG.SUCCESS:
                self.__reqCallback[resp.askid](True,self.__reqRetStr[resp.askid])
            else:
                self.__reqCallback[resp.askid](False,[])
            del self.__reqCallback[resp.askid]
            del self.__reqRetStr[resp.askid]
