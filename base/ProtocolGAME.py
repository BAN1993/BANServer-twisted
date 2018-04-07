import logging

import Base

HANLEN = 8

XYID_GAME_REQ_LOGIN = Base.XYID_GAME_BEGIN + 1 # 20002
XYID_GAME_RESP_LOGIN = Base.XYID_GAME_BEGIN + 2 # 20003
XYID_GAME_REQ_GOLD = Base.XYID_GAME_BEGIN + 3 # 20004
XYID_GAME_RESP_GOLD = Base.XYID_GAME_BEGIN + 4 # 20005

class ReqLogin(Base.protocolBase):
    connid = 0
    numid = 0
    userid = ""
    password = ""

    def make(self, data):
        try:
            self.makeBegin(data[8:])
            self.connid = self.getInt()
            self.numid = self.getInt()
            self.userid = self.getStr()
            self.password = self.getStr()
        except Base.protocolException, e:
            logging.error("ReqLogin err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_GAME_REQ_LOGIN)
        self.packInt(self.connid)
        self.packInt(self.numid)
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
            self.makeBegin(data[8:])
            self.connid = self.getInt()
            self.flag = self.getInt()
            self.numid = self.getInt()
        except Base.protocolException, e:
            logging.error("RespLogin err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_GAME_RESP_LOGIN)
        self.packInt(self.connid)
        self.packInt(self.flag)
        self.packInt(self.numid)
        return self.packEnd()

class ReqGold(Base.protocolBase):
    numid = 0

    def make(self, data):
        try:
            self.makeBegin(data[8:])
            self.numid = self.getInt()
        except Base.protocolException, e:
            logging.error("ReqGold err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_GAME_REQ_GOLD)
        self.packInt(self.numid)
        return self.packEnd()

class RespGold(Base.protocolBase):
    numid = 0
    gold = 0

    def make(self, data):
        try:
            self.makeBegin(data[8:])
            self.numid = self.getInt()
            self.gold = self.getInt()
        except Base.protocolException, e:
            logging.error("RespGold err,msg=" + e.msg)
            return False
        return True

    def pack(self):
        self.packBegin(XYID_GAME_RESP_GOLD)
        self.packInt(self.numid)
        self.packInt(self.gold)
        return self.packEnd()



