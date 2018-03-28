#encoding:utf-8

import logging

import ConnectorServer
import ConnectorClient
import PlayerManager
from CryptManager import gCrypt

class Server(object):

    m_port = 0
    m_connectorServer = None
    m_playerManager = None
    m_gameSvrClient = None

    m_gameSvrHost = ""
    m_gameSvrPort = 0
    m_gameServer = None

    def __init__(self,conf):
        self.m_port = int(conf.get("serverConfig", "port"))
        self.m_gameSvrHost = str(conf.get("GameServer","host"))
        self.m_gameSvrPort = int(conf.get("GameServer", "port"))
        logging.info("svrport=%d,gshost=%s,gspost=%d" % (self.m_port,self.m_gameSvrHost,self.m_gameSvrPort))
        self.m_connectorServer = ConnectorServer.ConnectorServer(self, self.m_port)
        self.m_gameServer  = ConnectorClient.ConnectorClient(self,self.m_gameSvrHost,self.m_gameSvrPort)
        self.m_playerManager = PlayerManager.PlayerManager(self)

        gCrypt.init(conf)

    def run(self):
        self.m_gameServer.connect()
        self.m_connectorServer.run()

    # Client
    def newClient(self,conn):
        self.m_playerManager.newClient(conn)

    def recvFromClient(self,conn,data):
        self.m_playerManager.recvFromClient(conn,data)

    def loseClient(self,conn):
        self.m_playerManager.loseClient(conn)

    # GameSver


