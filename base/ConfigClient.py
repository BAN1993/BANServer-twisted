#encoding:utf-8

import logging
import sys
sys.path.append("../base")

import ConnectorClient

class ConfigClent:

    m_subType = 0
    m_cfgIp = ""
    m_cfgPort = 0

    m_server = None
    m_conn = None

    __recvData = ""

    def __init__(self,server,subtype,cfgip,cfgport):
        self.m_server = server
        self.m_subType = subtype
        self.m_cfgIp = cfgip
        self.m_cfgPort = cfgport

    def connect(self):
        ConnectorClient.ConnectorClient(self, self.m_cfgIp, self.m_cfgPort)

    def newServer(self, conn):
        # TODO
        pass
