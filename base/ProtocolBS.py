#encoding:utf-8

import logging

import Base

XYID_REQ_AUTH = Base.XYID_BASE_BEGIN + 1 # 1002
XYID_RESP_AUTH = Base.XYID_BASE_BEGIN + 2 # 1003

class ReqAuth(Base.protocolBase):
    appid = 0
    svrtype = 0

    def make(self, data):
        try:
            self.makeBegin(data)
            self.appid = self.getInt()
            self.svrtype = self.getInt()
        except Base.protocolException, e:
            logging.error("ReqAuth err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_REQ_AUTH)
        self.packInt(self.appid)
        self.packInt(self.svrtype)
        return self.packEnd()

class RespAuth(Base.protocolBase):
    key = ""

    def make(self, data):
        try:
            self.makeBegin(data)
            self.key = self.getStr()
        except Base.protocolException, e:
            logging.error("RespAuth err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_RESP_AUTH)
        self.packStr(self.key)
        return self.packEnd()
