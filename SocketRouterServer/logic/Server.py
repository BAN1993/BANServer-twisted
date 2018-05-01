#encoding:utf-8

import sys
sys.path.append("../base")
import logging
from twisted.application.internet import TimerService

import Base
import ServerInterface
import ConnectorServer
import ConnectorClient
import ConfigClient
import PlayerManager
from CryptManager import gCrypt

class Server(ServerInterface.ServerBase,ServerInterface.ClientBase):

    m_isRunning = False

    m_config = None
    m_timer = None

    m_port = 0
    m_connectorServer = None
    m_playerManager = None
    #m_gameSvrClient = None

    m_centerCliHost = ""
    m_centerCliPort = 0
    m_centerClient = None

    def init(self,subtype,conf):
        cfgip = str(conf.get("configsvr", "host"))
        cfgport = int(conf.get("configsvr", "port"))
        self.m_config = ConfigClient.ConfigClent(self, subtype, Base.SVR_TYPE_SRS, cfgip, cfgport)

        self.m_connectorServer = ConnectorServer.ConnectorServer(self)
        self.m_centerClient = ConnectorClient.ConnectorClient(self)
        self.m_playerManager = PlayerManager.PlayerManager(self)
        gCrypt.init(conf)

    def timer(self):
        self.m_playerManager.timer()

    def run(self):
        self.m_config.connect(self.configCallBack)

        self.m_timer = TimerService(1, self.timer)
        self.m_timer.startService()

        #要放在最后一步
        from twisted.internet import reactor
        self.m_isRunning = True
        logging.info("reactor run")
        reactor.run()

    def configCallBack(self,flag):
        if flag:
            self.m_connectorServer.begin(self.m_config.getPort())

            sql = "SELECT CONCAT(cast(A.id AS CHAR),'$$$',cast(B.ip AS CHAR),'$$$',cast(A. PORT AS CHAR)) FROM config_svr A,config_routing_table B WHERE A.svrtype = 2 AND A.svrid = B.id"
            self.m_config.GetConfigBySql(sql,self.getGameServerConfigCB)
        else:
            logging.error("connect config error and return")
            self.stop()

    def getGameServerConfigCB(self,flag,retstr):
        if flag:
            strconfig = str(retstr[0])
            tab = strconfig.split("$$$")
            self.m_centerCliHost = str(tab[1])
            self.m_centerCliPort = int(tab[2])
            self.m_centerClient.connect(self.m_centerCliHost, self.m_centerCliPort)
        else:
            logging.error("get gameserver config error")
            self.stop()

    def stop(self):
        self.m_timer.stopService()
        if self.m_isRunning:
            from twisted.internet import reactor
            if not reactor._stopped :
                logging.info("stop reactor")
                reactor.stop()
            else:
                logging.info("try stop ractor,but is stopped")
        else:
            logging.info("try stop svr,but is not running")

    # Client
    def newClient(self,conn):
        self.m_playerManager.newClient(conn)

    def recvFromClient(self,conn,data):
        self.m_playerManager.recvFromClient(conn,data)

    def loseClient(self,conn):
        self.m_playerManager.loseClient(conn)

    # GameSver
    def newServer(self,conn):
        self.m_playerManager.newServer(conn)

    def lostServer(self,conn):
        logging.warning("lost server and try connect")
        self.m_centerClient.reConnect()

    def recvFromServer(self,conn,data):
        self.m_playerManager.recvFromServer(conn,data)

    def sendToServer(self,data):
        self.m_centerClient.sendData(data)

