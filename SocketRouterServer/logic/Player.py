
import logging

import Base
import Protocol

class Player:

    m_playerManager = None
    m_conn = None
    m_ip = ""
    m_numid = 0

    __recvBuf = ""
    __isAuth = False

    def __init__(self,manager,conn):
        self.m_playerManager = manager
        self.m_conn = conn
        self.m_ip = conn.transport.hostname

    def recvData(self,data):
        self.__recvBuf += data
        packlen = Base.getPackLen(self.__recvBuf)
        if packlen <= 0:
            return
        if packlen + Base.LEN_INT > len(self.__recvBuf):
            return
        data = self.__recvBuf[0: packlen + Base.LEN_INT]
        self.__recvBuf = self.__recvBuf[packlen + Base.LEN_INT:]
        ret, xyid, packlen, buf = Base.getXYHand(data)
        if ret:
            self.selectProtocol(xyid, buf[0: packlen])

    def sendData(self,data):
        self.m_conn.transport.write(data)

    def selectProtocol(self,xyid,data):
        logging.debug("xyid=%d" % xyid)
        if xyid == Protocol.XYID_REQLOGIN :
            req = Protocol.ReqLogin()
            ret = req.make(data)
            logging.info("numid=%d,userid=%s,pwd=%s" % (req.numid, req.userid, req.password))

            resp = Protocol.RespLogin()
            resp.flag = resp.FLAG.SUCCESS

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
                    resp.numid = int(rslt[0][0])
                    if gPlayerManager.addPlayer(conn, resp.numid):
                        gPlayerManager.broadcastPlayerData(conn, req.numid)
                else:
                    resp.flag = resp.FLAG.PWDERR
                    logging.info("numid=%d,userid=%s pwd err" % (req.numid, req.userid))
