#encoding:utf-8

import logging
import sys
sys.path.append("../base")

import Base
import ConnectorServer
import ProtocolCFG
from CryptManager import gCrypt
from DBManager import gDBManager

class Server(object):
    m_isRunning = False

    m_port = 0
    m_connectorServer = None
    m_svrDataList = {}  # [conn] = ""
    m_svrList = {} # [appid] = conn

    def init(self, conf):
        self.m_port = int(conf.get("serverConfig", "port"))
        logging.info("svrport=%d" % self.m_port)
        self.m_connectorServer = ConnectorServer.ConnectorServer(self, self.m_port)

        gCrypt.init(conf)
        gDBManager.init(conf)

    def run(self):
        self.m_connectorServer.begin()

        from twisted.internet import reactor
        self.m_isRunning = True
        reactor.run()

    def stop(self):
        if self.m_isRunning:
            from twisted.internet import reactor
            reactor.stop()

    def newClient(self,conn):
        logging.info("conn ip=%s" % conn.transport.hostname)
        self.m_svrDataList[conn] = ""

    def loseClient(self,conn):
        logging.info("conn ip=%s" % conn.transport.hostname)
        if self.m_svrDataList.has_key(conn):
            del self.m_svrDataList[conn]

    def recvFromClient(self, conn, data):
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
                self.selectProtocol(conn, data)
        else:
            logging.error("no data list")

    def selectProtocol(self,conn,buf):
        ret, packlen, appid, numid, xyid, data = Base.getXYHand(buf)
        if not ret:
            logging.warning("getXYHand error")
            return
        logging.debug("packlen=%d,appid=%d,numid=%d,xyid=%d" % (packlen,appid,numid,xyid))
        if xyid == ProtocolCFG.XYID_CFG_REQ_CONNECT:
            req = ProtocolCFG.ReqConnect()
            ret = req.make(data)
            logging.info("ReqConnect:subtype=%d,svrtype=%d,ip=%s" % (req.subtype,req.svrtype,conn.transport.hostname))

            resp = ProtocolCFG.RespConnect()

            #获取配置
            appid = 0
            port = 0
            config = ""
            sql = "select A.appid,A.port,A.config from config_svr A,config_routing_table B where A.subtype=%d and A.svrtype=%d and B.ip='%s' and A.svrid=B.id" % (req.subtype,req.svrtype,conn.transport.hostname)
            ret, row, rslt = gDBManager.select(sql)
            if not ret:
                resp.flag = resp.FLAG.DBERR
                logging.error("select ret err,sql=%s" % sql)
                buf = resp.pack()
                conn.transport.write(buf)
                return
            elif row <= 0:
                resp.flag = resp.FLAG.NOCONFIG
                logging.info("userid=%s select no data" % req.userid)
                buf = resp.pack()
                conn.transport.write(buf)
                return
            else:
                appid = int(rslt[0][0])
                port = int(rslt[0][1])
                config = rslt[0][2]
                logging.debug("appid=%d,port=%d,config=%s" % (appid,port,config))

            #验证appid
            if appid > 65535 or appid <=0:
                resp.flag = resp.FLAG.ERRAPPID
                logging.error("error appid,appid=%d" % appid)
                buf = resp.pack()
                conn.transport.write(buf)
                return

            #检查是否重复连接
            if self.m_svrList.has_key(appid):
                resp.flag = resp.FLAG.CONNECTED
                logging.warning("appid=%d had been connected" % appid)
                buf = resp.pack()
                conn.transport.write(buf)

            #这里将appid赋给conn.m_numid
            conn.m_numid = appid
            self.m_svrList[appid] = conn

            logging.info("auth success,flag=%d,appid=%d,port=%d,config=%s" % (resp.flag,resp.appid,resp.port,resp.config))
            resp.flag = resp.FLAG.SUCCESS
            resp.appid = appid
            resp.port = port
            resp.config = config
            buf = resp.pack()
            conn.transport.write(buf)
        elif xyid == ProtocolCFG.XYID_CFG_REQ_CONFIG:

            req = ProtocolCFG.ReqConfig()
            ret = req.make(data)
            logging.info("ReqConfig:sql=%s" % req.sqlstr)

            respFinish = ProtocolCFG.RespConfigFinish()

            if not self.m_svrList.has_key(conn.m_numid):
                logging.warning("conn is not in svrlist,sql=%s" % req.sqlstr)
                respFinish.flag = respFinish.FLAG.BAN
                buf = respFinish.pack()
                conn.transport.write(buf)
                return

            ret, row, rslt = gDBManager.select(req.sqlstr)
            if not ret:
                respFinish.flag = respFinish.FLAG.DBERR
                logging.error("select ret err,sql=%s" % req.sqlstr)
                buf = respFinish.pack()
                conn.transport.write(buf)
                return
            elif row <= 0:
                respFinish.flag = respFinish.FLAG.NOCONFIG
                logging.warning("had no config,sql=%s" % req.sqlstr)
                buf = respFinish.pack()
                conn.transport.write(buf)
                return
            else:
                resp = ProtocolCFG.RespConfig()
                for i in range(len(rslt)):
                    respFinish.count += 1
                    resp.retstr = rslt[i]
                    buf = resp.pack()
                    conn.transport.write(buf)

            respFinish.flag = respFinish.FLAG.SUCCESS
            buf = respFinish.pack()
            logging.info("appid=%d,flag=%d,count=%d" % (conn.m_numid,respFinish.flag,respFinish.count))
            conn.transport.write(buf)

        else:
            logging.warning("error xyid=%d" % xyid)
