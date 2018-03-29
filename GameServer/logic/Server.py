#encoding:utf-8

import logging

import ConnectorServer
import ConnectorClient
import PlayerManager
from CryptManager import gCrypt

class Server(object):

    m_port = 0
    m_connectorServer = None

    def __init__(self,conf):
        self.m_port = int(conf.get("serverConfig", "port"))
        logging.info("svrport=%d" % self.m_port)
        self.m_connectorServer = ConnectorServer.ConnectorServer(self, self.m_port)

        gCrypt.init(conf)

    def run(self):
        self.m_connectorServer.begin()

        from twisted.internet import reactor
        reactor.run()

    # Client
    def newClient(self,conn):
        logging.info("conn ip=%s,connid=%d" % (conn.transport.hostname))

    def recvFromClient(self,conn,data):
        self.m_playerManager.recvFromClient(conn,data)

    def loseClient(self,conn):
        logging.info("conn ip=%s,connid=%d" % (conn.transport.hostname))

    # GameSver


