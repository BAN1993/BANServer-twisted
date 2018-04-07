
import logging
import sys
sys.path.append("../base")

import Base
import Player
import ProtocolSRS
import ProtocolGAME


class PlayerManager(object):

    m_connid = 0
    m_unAuthList = {} # [connid] = player
    m_playerList = {} # [numid] = player

    m_server = None

    m_svrDataList = {} # [client conn] = ""

    def __init__(self,server):
        self.m_server = server

    def newClient(self,conn):
        pl = Player.Player(self, conn)
        self.m_connid += 1
        conn.m_connid = self.m_connid
        self.m_unAuthList[self.m_connid] = pl
        logging.info("conn ip=%s,connid=%d" % (conn.transport.hostname, self.m_connid))

        resp = ProtocolSRS.RespConnect()
        resp.connid = self.m_connid
        buf = resp.pack()
        pl.sendData(buf)

    def recvFromClient(self,conn,data):
        logging.debug("numid=%d,connid=%d" % (conn.m_numid,conn.m_connid))
        if self.m_playerList.has_key(conn.m_numid):
            self.m_playerList[conn.m_numid].recvData(data)
        else:
            if self.m_unAuthList.has_key(conn.m_connid):
                self.m_unAuthList[conn.m_connid].recvData(data)
            else:
                logging.warn("can not find conn in two list,numid=%d,connid=%d,ip=%s" % (conn.m_numid, conn.m_connid, conn.transport.hostname))

    def loseClient(self,conn):
        numid = conn.m_numid
        connid = conn.m_connid
        if self.m_unAuthList.has_key(connid):
            logging.info("loseconn connid=%d,ip=%s,del from unauthlist" % (connid, conn.transport.hostname))
            del self.m_unAuthList[connid]
        if self.m_playerList.has_key(numid):
            logging.info("loseconn numid=%d,ip=%s,del from playerlist" % (numid, conn.transport.hostname))
            del self.m_playerList[numid]

    def newServer(self,conn):
        self.m_svrDataList[conn] = ""

    def recvFromServer(self,conn,data):
        if self.m_svrDataList.has_key(conn):
            self.m_svrDataList[conn] += data
            while True:
                packlen = Base.getPackLen(self.m_svrDataList[conn])
                if packlen <= 0:
                    return
                if packlen + Base.LEN_INT > len(self.m_svrDataList[conn]):
                    return

                data = self.m_svrDataList[conn][0: packlen + Base.LEN_INT]
                self.m_svrDataList[conn] = self.m_svrDataList[conn][packlen + Base.LEN_INT:]
                ret, xyid, packlen, buf = Base.getXYHand(data)
                if ret == False:
                    continue
                self.selectProtocol(xyid, buf[0: packlen])
        else:
            logging.error("no data list")

    def selectProtocol(self,xyid,data):
        if xyid == ProtocolGAME.XYID_GAME_RESP_LOGIN:
            mpc = ProtocolGAME.RespLogin()
            ret = mpc.make(data)
            logging.debug("connid=%d,flag=%d,numid=%d" % (mpc.connid, mpc.flag, mpc.numid))

            pl = None
            if self.m_unAuthList.has_key(mpc.connid):
                pl = self.m_unAuthList[mpc.connid]
            else:
                logging.error("can not find in auth list,connid=%d" % mpc.connid)
                return

            if mpc.flag == mpc.FLAG.SUCCESS and ret:
                self.m_playerList[mpc.numid] = pl
                del self.m_unAuthList[mpc.connid]
            else:
                logging.warning("login err,connid=%d,flag=%d,numid=%d" % (mpc.connid, mpc.flag, mpc.numid))

            resp = ProtocolSRS.RespLogin()
            resp.numid = mpc.numid
            resp.flag = mpc.flag
            buf = resp.pack()
            pl.sendData(buf)



