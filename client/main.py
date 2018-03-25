from twisted.internet.protocol import Protocol, ClientFactory

gIp = "127.0.0.1"
gPort = 8300

class mProtocol(Protocol):

    def connectionMade(self):
        data = raw_input("send:")
        self.transport.write(data)

    def dataReceived(self, data):
        print("recv data:",data)

    def connectionLost(self, reason):
        print("connect close")


class mFactory(ClientFactory):

    protocol = mProtocol

    def clientConnectionFailed(self, connector, reason):
        print("clientConnectionFailed")

def main():

    factory = mFactory()
    from twisted.internet import reactor
    reactor.connectTCP(gIp,gPort,factory)
    reactor.run()


if __name__ == '__main__':
    main()
