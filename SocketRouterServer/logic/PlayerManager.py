
import logging

import Player
import ProtocolSRS

class PlayerManager(object):

    m_connid = 0
    m_unAuthList = {} # [connid] = player
    m_playerList = {} # [numid] = player

    m_server = None

    def __init__(self,server):
        self.m_server = server

    def newClient(self,conn):
        pl = Player.Player(self, conn)
        self.m_connid += 1
        self.m_unAuthList[self.m_connid] = pl
        logging.info("conn ip=%s,connid=%d" % (conn.transport.hostname, self.m_connid))

        resp = ProtocolSRS.RespConnect()
        resp.connid = self.m_connid
        buf = resp.pack()
        pl.sendData(buf)

    def recvFromClient(self,conn,data):
        if self.m_playerList.has_key(conn.m_numid):
            self.m_playerList[conn.m_numid].recvData(data)
        else:
            if self.m_unAuthList.has_key(conn.m_connid):
                self.m_unAuthList[conn.m_connid].recvData(data)
            else:
                logging.warn("can not find conn in two list,numid=%d,connid=%d,ip=%s" % conn.m_numid, conn.m_connid, conn.transport.hostname)



    def loseClient(self,conn):
        numid = conn.m_numid
        connid = conn.m_connid
        if self.m_unAuthList.has_key(connid):
            logging.info("loseconn connid=%d,ip=%s,del from unauthlist" % connid, conn.transport.hostname)
            del self.m_unAuthList[connid]
        if self.m_playerList.has_key(numid):
            logging.info("loseconn numid=%d,ip=%s,del from playerlist" % numid, conn.transport.hostname)
            del self.m_playerList[numid]

    def recvFromServer(self,data):
        logging.debug(data)