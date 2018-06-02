#encoding:utf-8

from abc import ABCMeta, abstractmethod

class ServerBase(object):
    """
    server基类
    所有server都要继承并实现
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def newClient(self,conn):
        """
        新的客户端连接
        :param conn: ConnectServerProtocl
        :return: void
        """
        pass

    @abstractmethod
    def recvFromClient(self,conn,packlen,appid,numid,xyid,data):
        """
        收到消息
        :param conn:        ConnectServerProtocl
        :param packlen:     协议体长度
        :param appid:       目标appid
        :param numid:       账号
        :param xyid:        协议号
        :param data:        协议体
        :return:
        """
        pass

    @abstractmethod
    def loseClient(self,conn):
        """
        与客户端失去连接
        :param conn: ConnectServerProtocl
        :return: void
        """
        pass

class ClientBase(object):
    """
    client基类
    服务端不需要继承此类
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def connectSuccess(self,appid,client,flag):
        """
        成功连接到server
        :param appid: server id
        :param client: ConnectorClient
        :param flag: bool,连接是否成功
        :return: void
        """
        pass

    @abstractmethod
    def connectLost(self,appid,client):
        """
        失去和server的连接
        :param appid: server id
        :param client: ConnectorClient
        :return: void
        """
        pass

    @abstractmethod
    def recvData(self,packlen,appid,srcappid,numid,xyid,data):
        """
        收到消息
        :param packlen:     协议体长度
        :param appid:       目标appid
        :param srcappid:    来源appid
        :param numid:       账号
        :param xyid:        协议号
        :param data:        协议体
        :return:
        """
        pass

class ClientManager(object):
    """
    client管理类
    连接其他服务需要继承此类
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def recvData(self,packlen,appid,srcappid,numid,xyid,data):
        """
        收到消息
        :param packlen:     协议体长度
        :param appid:       目标appid
        :param srcappid:    来源appid
        :param numid:       账号
        :param xyid:        协议号
        :param data:        协议体
        :return:
        """
        pass
        

