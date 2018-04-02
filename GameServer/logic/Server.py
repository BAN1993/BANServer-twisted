#encoding:utf-8

import logging

import ConnectorServer
#from CryptManager import gCrypt

class Server(object):

    m_port = 0
    m_connectorServer = None

    def __init__(self,conf):
        self.m_port = int(conf.get("serverConfig", "port"))
        logging.info("svrport=%d" % self.m_port)
        self.m_connectorServer = ConnectorServer.ConnectorServer(self, self.m_port)

        #gCrypt.init(conf)

    def run(self):
        self.m_connectorServer.begin()

        from twisted.internet import reactor
        reactor.run()

    # Client
    def newClient(self,conn):
        logging.info("conn ip=%s" % (conn.transport.hostname))

    def recvFromClient(self,conn,data):
        logging.info("conn ip=%s,data=%s" % conn.transport.hostname,data)

    def loseClient(self,conn):
        logging.info("conn ip=%s" % (conn.transport.hostname))

    # GameSver


