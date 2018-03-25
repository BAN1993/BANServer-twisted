# coding=utf8
#实现了私聊，公聊。用户名密码存在redis。为了拓展，做了简单的模块。

from twisted.internet import reactor, defer
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory, Protocol, ServerFactory
import redis


class Server(ServerFactory):
    def __init__(self):
        self.users = {}
        self.last_messages = {}
        self.__db = dbServer

    # def start(self):

    # def stop(self):

    def do_login(self, pro, args):
        username, passwd = args
        if self.__db.get(username) is not None:
            if passwd != self.__db.get(username):
                return "do_login", False, "login failed"
            else:
                user = User(username, passwd, pro, 1)
                self.users[username] = user
                pro.user = user
                return "do_login", True, "login success"
        else:
            self.__db.set(username, passwd)
            self.__db.save()
        user = User(username, passwd, pro, 1)
        self.users[username] = user
        pro.user = user
        return "do_login", True, "login success"

    def checklogin(self, user):
        return user.logined

    def do_privatemsg(self, pro, args):
        target, msg = args
        user = pro.user
        if self.checklogin(user):
            self.last_messages[user] = msg
            msg = '[' + user.name + ']' + msg
            return "do_privatemsg", self.users[target], msg

    def do_publicmsg(self, pro, args):
        msg = args
        user = pro.user
        print user.name
        if self.checklogin(user):
            self.last_messages[user] = msg
            msg = '[' + user.name + ']' + msg[0]
            return "do_publicmsg", self.users.values(), msg


class User(object):
    def __init__(self, name, passwd, pro, logined):
        self.name = name
        self.password = passwd
        self.nick_name = '&&' + name + '&&'
        self.proto = pro
        self.logined = logined


class ChatProtocol(LineReceiver):
    # line format: "func target_name *contents"
    # example: "privatemsg hs how are you....."
    # example: "publicmsg how are you....."
    # example: "login hs password"
    def __init__(self):
        self.user = 0
        self.pro = self

    def connectionMade(self):
        self.sendLine("please input: 'login,username,password'")

    def lineReceived(self, line):
        defer.maybeDeferred(self.parse, line).addCallback(self.processor).addCallback(self.ack)

    def parse(self, line):
        result = line.split(',')
        func = result[0]
        args = result[1:]
        return func, args

    def processor(self, args):
        func, arg = args
        _func = getattr(server, 'do_' + func)
        if _func:
            return _func(self.pro, arg)
        else:
            raise Exception("xxxxx")

    def ack(self, args):
        func, target, msg = args
        if func == 'do_login':
            if not target:
                self.kickOut()
            self.sendLine(msg)
        elif func == 'do_privatemsg':
            target.proto.sendLine(msg)
        elif func == 'do_publicmsg':
            for user in target:
                if user.proto != self:
                    user.proto.sendLine(msg)
        else:
            pass

    def kickOut(self):
        self.sendLine('passwd is wrong')
        self.transport.loseConnection()


class redisServer(object):
    def __init__(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        self.db = r

    def set(self, key, value):
        self.db.set(key, value)

    def save(self):
        self.db.save()

    def get(self, key):
        return self.db.get(key)


dbServer = redisServer()
server = Server()
server.protocol = ChatProtocol
reactor.listenTCP(8008, server)
print 'server start!'
reactor.run()