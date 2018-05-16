using System;
using System.Net;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SocketClient
{
    class Client
    {
        private byte[] result = new byte[1024];
        private SocketManager m_socket = new SocketManager();
        private int m_connid;

        public void start()
        {
            Cryptor crypt = Cryptor.getInstance();
            crypt.setAESKey("SocketRouterSvr");

            m_socket.init("127.0.0.1", 8300);
            m_socket.setRecvCallback(recv);
            m_socket.connect();
            m_socket.loop();

            /*
            {
                //测试登录
                ReqLogin pack = new ReqLogin(connid, "test3003", "123456");
                byte[] buf = pack.pack();
                clientSocket.Send(buf);

                int receiveLength = clientSocket.Receive(result);
                ushort len = System.BitConverter.ToUInt16(result, 0);
                byte[] packbuf = new byte[len];
                Array.Copy(result, 2, packbuf, 0, len);
                string decstr = "";
                crypt.decryptAES(packbuf, out decstr);

                RespLogin resp = new RespLogin();
                resp.make(UTF8Encoding.UTF8.GetBytes(decstr));
                Console.WriteLine("登录回复:flag=" + resp.flag + ",numid=" + resp.numid);
            }
            */

            Console.ReadKey();
        }

        public void recv(byte[] buf)
        {
            RespConnect respConnect = new RespConnect();
            respConnect.make(buf);
            Console.WriteLine("连接回复:connid=" + respConnect.connid);
            m_connid = respConnect.connid;
        }

    }
}
