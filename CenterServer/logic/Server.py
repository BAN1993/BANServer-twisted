#encoding:utf-8

import sys
sys.path.append("../base")
import logging
from twisted.application.internet import TimerService

import Base
import ServerInterface
import ConnectorServer
import ConfigClient
import ProtocolSRS
from CryptManager import gCrypt
from DBManager import gDBManager

class Server(ServerInterface.ServerBase):

    m_isRunning = False

    m_config = None
    m_timer = None

    m_port = 0
    m_connectorServer = None
    m_svrDataList = {} # [client conn] = ""

    def init(self, subtype, conf):
        cfgip = str(conf.get("configsvr", "host"))
        cfgport = int(conf.get("configsvr", "port"))
        self.m_config = ConfigClient.ConfigClent(self,subtype,Base.SVR_TYPE_CENTER,cfgip,cfgport)

        self.m_connectorServer = ConnectorServer.ConnectorServer(self)

        gCrypt.init(conf)
        #gDBManager.init(conf)

    def run(self):
        self.m_config.connect(self.configCallBack)

        # 要放在最后一步
        from twisted.internet import reactor
        self.m_isRunning = True
        logging.info("reactor run")
        reactor.run()

    def timer(self):
        pass

    def configCallBack(self,flag):
        if flag:
            configstr = self.m_config.getConfig()
            configstr = "{" + configstr + "}"
            tab = eval(configstr)
            if tab.has_key('dbip') and tab.has_key('dbport') and tab.has_key('dbuser') and tab.has_key('dbpwd') and tab.has_key('dbname'):
                gDBManager.init(tab['dbip'],tab['dbport'],tab['dbuser'],tab['dbpwd'],tab['dbname'])
            else:
                logging.error("db config error")
                self.stop()
                return
            self.m_connectorServer.begin(self.m_config.getPort())

            self.m_timer = TimerService(1, self.timer)
            self.m_timer.startService()
        else:
            logging.error("connect config error and return")
            self.stop()

    def stop(self):
        self.m_timer.stopService()
        if self.m_isRunning:
            from twisted.internet import reactor
            if not reactor._stopped :
                logging.info("stop reactor")
                reactor.stop()
            else:
                logging.info("try stop ractor,but is stopped")
        else:
            logging.info("try stop svr,but is not running")

    def newClient(self,conn):
        logging.info("conn ip=%s" % conn.transport.hostname)
        self.m_svrDataList[conn] = ""

    def recvFromClient(self,conn,data):
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

    def loseClient(self,conn):
        logging.info("conn ip=%s" % (conn.transport.hostname))
        if self.m_svrDataList.has_key(conn):
            del self.m_svrDataList[conn]

    def selectProtocol(self,conn,buf):
        ret, packlen, appid, numid, xyid, data = Base.getXYHand(buf)
        if not ret:
            logging.warning("getXYHand error")
            return
        logging.debug("packlen=%d,appid=%d,numid=%d,xyid=%d" % (packlen,appid,numid,xyid))
        if xyid == ProtocolSRS.XYID_SRS_REQ_LOGIN:
            req = ProtocolSRS.ReqLogin()
            ret = req.make(data)
            logging.info("ReqLogin:connid=%d,userid=%s,pwd=%s" % (req.connid, req.userid, req.password))

            resp = ProtocolSRS.RespLogin()
            resp.connid = req.connid

            sql = "select numid,passwd from players where userid='%s'" % req.userid
            ret, row, rslt = gDBManager.select(sql)
            if not ret:
                resp.flag = resp.FLAG.DBERR
                logging.error("select ret err,sql=%s" % sql)
            elif row <= 0:
                resp.flag = resp.FLAG.NOUSER
                logging.info("userid=%s select no data" % req.userid)
            else:
                if str(rslt[0][1]) == req.password:
                    resp.flag = resp.FLAG.SUCCESS
                    resp.numid = int(rslt[0][0])
                    logging.info("userid=%s login success,numid=%d" % (req.userid,resp.numid))
                else:
                    resp.flag = resp.FLAG.PWDERR
                    logging.info("userid=%s pwd err" % req.userid)

            buf = resp.pack()
            conn.transport.write(buf)

        else:
            logging.warning("unknown xy,xyid=%d" % xyid)

