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
        print("port=%d" % (self.m_port))
        self.m_connector = connector.Connector(self)
        self.m_playerManager = playerManager.playerManager(self)

    def run(self):
        self.m_connector.run()

    def newConnect(self,protocol):
        print("new connect:",protocol)

    def recvData(self,protocol,data):
        print("recv data:", protocol,",data:",data)
        protocol.transport.write("hello")

    def loseConnect(self,protocol):
        print("lose connect:", protocol)
