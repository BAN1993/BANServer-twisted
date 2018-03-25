#encoding:utf-8

import logging

import connector
import playerManager

class Server(object):

    m_port = 0
    m_connector = None
    m_playerManager = None

    def __init__(self,conf):
        self.m_port = int(conf.get("serverConfig", "port"))
        logging.info("port=%d" % (self.m_port))
        self.m_connector = connector.Connector(self)
        self.m_playerManager = playerManager.playerManager(self)

    def run(self):
        self.m_connector.run()

    def newConnect(self,conn):
        self.m_playerManager.newConnect(conn)

    def recvData(self,conn,data):
        self.m_playerManager.recvData(conn,data)

    def loseConnect(self,conn):
        self.m_playerManager.loseConnect(conn)
