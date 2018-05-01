#encoding:utf-8

import logging

import Base

XYID_SRS_RESP_CONNECT = Base.XYID_SRS_BEGIN + 1 # 10002
XYID_SRS_REQ_LOGIN = Base.XYID_SRS_BEGIN + 2
XYID_SRS_RESP_LOGIN = Base.XYID_SRS_BEGIN + 3
XYID_SRS_REQ_REGISTER = Base.XYID_SRS_BEGIN + 4
XYID_SRS_RESP_REGISTER = Base.XYID_SRS_BEGIN + 5

class RespConnect(Base.protocolBase):
    connid = 0

    def make(self, data):
        try:
            self.makeBegin(data)
            self.connid = self.getInt()
        except Base.protocolException, e:
            logging.error("RespConnect err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_SRS_RESP_CONNECT)
        self.packInt(self.connid)
        return self.packEnd()

class ReqLogin(Base.protocolBase):
    connid = 0
    userid = ""
    password = ""

    def make(self, data):
        try:
            self.makeBegin(data)
            self.connid = self.getInt()
            self.userid = self.getStr()
            self.password = self.getStr()
        except Base.protocolException, e:
            logging.error("ReqLogin err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_SRS_REQ_LOGIN)
        self.packInt(self.connid)
        self.packStr(self.userid)
        self.packStr(self.password)
        return self.packEnd()

class RespLogin(Base.protocolBase):
    FLAG = Base.getEnum(SUCCESS=0,
                        NOUSER=1,
                        PWDERR=2,
                        DBERR=3)
    connid = 0
    flag = 0
    numid = 0

    def make(self, data):
        try:
            self.makeBegin(data)
            self.connid = self.getInt()
            self.flag = self.getInt()
            self.numid = self.getInt()
        except Base.protocolException, e:
            logging.error("RespLogin err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_SRS_RESP_LOGIN)
        self.packInt(self.connid)
        self.packInt(self.flag)
        self.packInt(self.numid)
        return self.packEnd()

class ReqRegister(Base.protocolBase):
    userid = ""
    password = ""

    def make(self, data):
        try:
            self.makeBegin(data)
            self.userid = self.getStr()
            self.password = self.getStr()
        except Base.protocolException, e:
            logging.error("ReqRegister err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_SRS_REQ_REGISTER)
        self.packStr(self.userid)
        self.packStr(self.password)
        return self.packEnd()

class RespRegister(Base.protocolBase):
    FLAG = Base.getEnum(SUCCESS=0,
                        USED_USERID=1,
                        DBERR=2,
                        CREATEERR=3)
    flag = 0
    numid = 0

    def make(self, data):
        try:
            self.makeBegin(data)
            self.flag = self.getInt()
            self.numid = self.getInt()
        except Base.protocolException, e:
            logging.error("RespRegister err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_SRS_RESP_REGISTER)
        self.packInt(self.flag)
        self.packInt(self.numid)
        return self.packEnd()


