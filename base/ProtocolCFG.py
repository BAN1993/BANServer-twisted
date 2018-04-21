#encoding:utf-8

import logging

import Base

XYID_CFG_REQ_CONNECT = Base.XYID_CFG_BEGIN + 1 # 102 请求连接
XYID_CFG_RESP_CONNECT = Base.XYID_CFG_BEGIN + 2 # 103
XYID_CFG_REQ_CONFIG = Base.XYID_CFG_BEGIN + 3 # 104 请求配置
XYID_CFG_RESP_CONFIG = Base.XYID_CFG_BEGIN + 4 # 105
XYID_CFG_RESP_CONFIGFINISH = Base.XYID_CFG_BEGIN + 5 # 106

class ReqConnect(Base.protocolBase):

    subtype = 0
    svrtype = 0

    def make(self, data):
        try:
            self.makeBegin(data)
            self.subtype = self.getInt()
            self.svrtype = self.getInt()
        except Base.protocolException, e:
            logging.error("ReqConnect err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_CFG_REQ_CONNECT)
        self.packInt(self.subtype)
        self.packInt(self.svrtype)
        return self.packEnd()

class RespConnect(Base.protocolBase):
    FLAG = Base.getEnum(SUCCESS=0,
                        DBERR=1,
                        NOCONFIG=2,
                        CONNECTED=3,
                        ERRAPPID=4)
    flag = 0
    appid = 0
    port = 0
    config = ""

    def make(self,data):
        try:
            self.makeBegin(data)
            self.flag = self.getInt()
            self.appid = self.getUShort()
            self.port = self.getInt()
            self.config = self.getStr()
        except Base.protocolException, e:
            logging.error("RespConnect err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_CFG_RESP_CONNECT)
        self.packInt(self.flag)
        self.packUShort(self.appid)
        self.packInt(self.port)
        self.packStr(self.config)
        return self.packEnd()

class ReqConfig(Base.protocolBase):
    sqlstr = ""

    def make(self,data):
        try:
            self.makeBegin(data)
            self.sqlstr = self.getStr()
        except Base.protocolException, e:
            logging.error("ReqConfig err,msg="+e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_CFG_REQ_CONFIG)
        self.packStr(self.sqlstr)
        return self.packEnd()

class RespConfig(Base.protocolBase):
    retstr = ""

    def make(self,data):
        try:
            self.makeBegin(data)
            self.retstr = self.getStr()
        except Base.protocolException, e:
            logging.error("RespConfig err,msg="+e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_CFG_RESP_CONFIG)
        self.packStr(self.retstr)
        return self.packEnd()

class RespConfigFinish(Base.protocolBase):
    FLAG = Base.getEnum(SUCCESS=0,
                        DBERR=1,
                        NOCONFIG=2,
                        BAN=3)
    flag = 0
    count = 0

    def make(self,data):
        try:
            self.makeBegin(data)
            self.flag = self.getInt()
            self.count = self.getInt()
        except Base.protocolException, e:
            logging.error("RespConfigFinish err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_CFG_RESP_CONFIGFINISH)
        self.packInt(self.flag)
        self.packInt(self.count)
        return self.packEnd()
