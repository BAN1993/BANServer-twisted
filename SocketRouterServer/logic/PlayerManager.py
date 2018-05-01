#encoding:utf-8

import logging
import sys
sys.path.append("../base")

import Base
import Player
import ProtocolSRS


class PlayerManager(object):

    m_connid = 0
    m_unAuthList = {} # [connid] = player
    m_playerList = {} # [numid] = player

    m_server = None

    m_svrDataList = {} # [client conn] = ""

    def __init__(self,server):
        self.m_server = server

    def timer(self):
        logging.debug("unauth count=%d,player count=%d" % (self.m_unAuthList.__len__(),self.m_playerList.__len__()))

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
        logging.debug("numid=%d,connid=%d,conn=%s" % (conn.m_numid,conn.m_connid,str(conn)))
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
                if packlen + Base.LEN_SHORT > len(self.m_svrDataList[conn]):
                    return

                data = self.m_svrDataList[conn][0: packlen + Base.LEN_SHORT]
                self.m_svrDataList[conn] = self.m_svrDataList[conn][packlen + Base.LEN_SHORT:]
                self.selectProtocol(data)
        else:
            logging.error("no data list")

    def selectProtocol(self,buf):
        #现在appid还没用,后面多个服务时会用到
        ret, packlen, appid, numid, xyid, data = Base.getXYHand(buf)
        if not ret:
            logging.warning("getXYHand error")
            return
        logging.debug("packlen=%d,appid=%d,numid=%d,xyid=%d" % (packlen,appid,numid,xyid))
        #处理特殊逻辑用
        if xyid == ProtocolSRS.XYID_SRS_RESP_LOGIN :
            mpc = ProtocolSRS.RespLogin()
            ret = mpc.make(data)
            logging.debug("connid=%d,flag=%d,numid=%d" % (mpc.connid, mpc.flag, mpc.numid))

            pl = None
            if self.m_unAuthList.has_key(mpc.connid):
                pl = self.m_unAuthList[mpc.connid]
            else:
                logging.error("can not find in auth list,connid=%d" % mpc.connid)
                return

            if mpc.flag == mpc.FLAG.SUCCESS and ret:
                pl.setPlayerData(mpc.numid)
                self.m_playerList[mpc.numid] = pl
                del self.m_unAuthList[mpc.connid]
                logging.info("add new player,numid=%d" % mpc.numid)
            else:
                logging.warning("login err,connid=%d,flag=%d,numid=%d" % (mpc.connid, mpc.flag, mpc.numid))

            #原样下发
            pl.sendData(buf)

        else:
            if self.m_playerList.has_key(numid):
                pl = self.m_playerList[numid]
                pl.sendData(buf)
            else:
                logging.warning("have no user numid=%d" % numid)




