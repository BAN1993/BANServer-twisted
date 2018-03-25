
import logging

class Player:

    m_playerManager = None
    m_conn = None
    m_ip = ""
    m_numid = 0

    __recvBuf = ""

    def __init__(self,manager,conn):
        self.m_playerManager = manager
        self.m_conn = conn
        self.m_ip = conn.transport.hostname

    def recvData(self,data):
        self.__recvBuf += data

    def __parserData(self):
        pass

