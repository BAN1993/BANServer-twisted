
import logging

import player

class playerManager(object):

    m_playerList = {}
    m_server = None

    def __init__(self,server):
        self.m_server = server

    def newConnect(self,conn):
        pl = player.Player(self,conn)
        self.m_playerList[conn] = pl
        logging.info("conn ip=%s" % conn.transport.hostname)

    def recvData(self,conn,data):
        if self.m_playerList.has_key(conn):
            self.m_playerList[conn].recvData(data)
        else:
            logging.warn("can not find conn in list,ip=%s" % conn.transport.hostname)


    def loseConnect(self,conn):
        if self.m_playerList.has_key(conn):
            logging.info("conn ip=%s" % conn.transport.hostname)
            del self.m_playerList[conn]
