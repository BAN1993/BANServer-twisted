#encoding:utf-8

import logging
import sys
sys.path.append("../..")

import Base
import DBManager
import ConnectorServer
import ProtocolSRS
import ProtocolGAME
from CryptManager import gCrypt
from DBManager import gDBManager

class Server(object):

    m_port = 0
    m_connectorServer = None
    m_svrDataList = {} # [client conn] = ""

    def __init__(self,conf):
        self.m_port = int(conf.get("serverConfig", "port"))
        logging.info("svrport=%d" % self.m_port)
        self.m_connectorServer = ConnectorServer.ConnectorServer(self, self.m_port)

        gCrypt.init(conf)
        gDBManager.init(conf)

    def run(self):
        self.m_connectorServer.begin()

        from twisted.internet import reactor
        reactor.run()

    def newClient(self,conn):
        logging.info("conn ip=%s" % (conn.transport.hostname))
        self.m_svrDataList[conn] = ""

    def recvFromClient(self,conn,data):
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
                self.selectProtocol(conn, xyid, buf[0: packlen])
        else:
            logging.error("no data list")

    def loseClient(self,conn):
        logging.info("conn ip=%s" % (conn.transport.hostname))

    def selectProtocol(self,conn,xyid,data):
        logging.debug("xyid=%d" % xyid)
        if xyid == ProtocolGAME.XYID_GAME_REQ_LOGIN :
            req = ProtocolGAME.ReqLogin()
            ret = req.make(data)
            logging.info("connid=%d,numid=%d,userid=%s,pwd=%s" % (req.connid,req.numid, req.userid, req.password))

            resp = ProtocolGAME.RespLogin()
            resp.connid = req.connid

            sql = "select numid,passwd from players where userid='%s'" % req.userid
            ret, row, rslt = gDBManager.select(sql)
            if not ret:
                resp.flag = resp.FLAG.DBERR
                logging.error("select ret err,sql=%s" % sql)
            elif row <= 0:
                resp.flag = resp.FLAG.NOUSER
                logging.info("numid=%d,userid=%s select no data" % (req.numid, req.userid))
            else:
                if str(rslt[0][1]) == req.password:
                    resp.flag = resp.FLAG.SUCCESS
                    resp.numid = int(rslt[0][0])
                    logging.info("numid=%d,userid=%s login success" % (req.numid, req.userid))
                else:
                    resp.flag = resp.FLAG.PWDERR
                    logging.info("numid=%d,userid=%s pwd err" % (req.numid, req.userid))

            buf = resp.pack()
            conn.transport.write(buf)

