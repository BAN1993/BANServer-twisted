#encoding:utf-8

import logging
import sys
sys.path.append("../base")

import Base
import ConnectorServer
import ConnectorClient
import ConfigClient
import PlayerManager
from CryptManager import gCrypt

class Server(object):

    m_isRunning = False

    m_config = None

    m_port = 0
    m_connectorServer = None
    m_playerManager = None
    m_gameSvrClient = None

    m_gameSvrHost = ""
    m_gameSvrPort = 0
    m_gameServer = None

    def init(self,subtype,conf):
        cfgip = str(conf.get("configsvr", "host"))
        cfgport = int(conf.get("configsvr", "port"))
        #logging.info("svrport=%d,gshost=%s,gspost=%d" % (self.m_port, self.m_gameSvrHost, self.m_gameSvrPort))
        #self.m_connectorServer = ConnectorServer.ConnectorServer(self, self.m_port)
        #self.m_gameServer = ConnectorClient.ConnectorClient(self, self.m_gameSvrHost, self.m_gameSvrPort)
        self.m_config = ConfigClient.ConfigClent(self,subtype,Base.SVR_TYPE_SRS,cfgip,cfgport)
        self.m_playerManager = PlayerManager.PlayerManager(self)
        gCrypt.init(conf)

    def run(self):
        self.m_config.connect(self.configCallBack)

        #要放在最后一步
        from twisted.internet import reactor
        self.m_isRunning = True
        reactor.run()

    def configCallBack(self,flag):
        if flag:
            self.m_gameServer.connect()
            self.m_connectorServer.begin()
        else:
            logging.error("connect config error and return")
            from twisted.internet import reactor
            reactor.stop()

    def stop(self):
        if self.m_isRunning:
            from twisted.internet import reactor
            reactor.stop()

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

    def recvFromServer(self,conn,data):
        self.m_playerManager.recvFromServer(conn,data)

    def sendToServer(self,data):
        self.m_gameServer.sendData(data)

