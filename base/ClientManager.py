#encoding:utf-8

import sys
sys.path.append("../base")
import logging

import Base
import ServerInterface
import ConnectorClient

"""
    连接客户端管理类
    1.支持多个连接
"""

class ClientStruct:
    appid = 0
    host = ""
    port = 0
    def __init__(self,appid,host,port):
        self.appid = appid
        self.host = host
        self.port = port
        pass

class ClientManager(ServerInterface.ClientBase):

    m_StructList = {} # [appid] = ClientStruct
    m_ClientList = {} # [appid] = ConnectorClient

    def addConnect(self,appid,host,port):
        if self.m_StructList.has_key(appid):
            logging.warning("appid=%s is in list" % appid)
            return
        else:
            cstruct = ClientStruct(appid,host,port)
            m_StructList[appid] = cstruct

            client = ConnectorClient.ConnectorClient(self)
            client.connect(appid,host,port)
        
        

    def sendData(self,buf,appid=0):
        pass

    def connectSuccess(self,appid,client):
        pass

    def lostServer(self,appid,conn):
        pass

    def recvFromServer(self,appid,conn,data):
        pass
