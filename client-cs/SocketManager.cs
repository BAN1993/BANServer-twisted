using System;
using System.Net;
using System.Net.Sockets;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SocketClient
{
    class SocketManager
    {
        private IPAddress m_ip = null;
        private int m_port = 0;
        private Socket m_socket = null;
        private string m_strBuf;
        private Cryptor m_crypt;
        
        public bool init(string ip, int port)
        {
            m_ip = IPAddress.Parse(ip);
            m_port = port;
            m_socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            m_crypt = Cryptor.getInstance();

            return true;
        }

        public bool connect()
        {
            try
            {
                m_socket.Connect(new IPEndPoint(m_ip, m_port));
                Console.WriteLine("连接服务器成功");
            }
            catch
            {
                Console.WriteLine("连接服务器失败，请按回车键退出！");
                return false;
            }
            return true;
        }

        public void loop()
        {
            while(true)
            {
                byte[] buf = new byte[1024];
                m_socket.Receive(buf);
                string strbuf = Encoding.UTF8.GetString(buf).TrimEnd('\0');
                m_strBuf = m_strBuf + strbuf;
                string outstr;
                while(getPacketBuf(out outstr))
                {
                    recvcallback(UTF8Encoding.UTF8.GetBytes(outstr));
                }
            }
        }

        public bool getPacketBuf(out string buf)
        {
            buf = "";
            if (m_strBuf.Length < 2)
                return false;
            string lenstr = m_strBuf.Substring(0, 2);
            ushort len = System.BitConverter.ToUInt16(UTF8Encoding.UTF8.GetBytes(lenstr), 0);
            byte[] packbuf = new byte[len];
            if (m_strBuf.Length < len + 2)
                return false;
            Array.Copy(UTF8Encoding.UTF8.GetBytes(m_strBuf), 2, packbuf, 0, len);
            m_crypt.decryptAES(packbuf, out buf);

            int buflen = m_strBuf.Length;
            if (buflen == len + 2)
            {
                m_strBuf = "";
            }
            else
            {
                m_strBuf = m_strBuf.Substring(len + 2, buflen);
            }
            return true;
        }

        //recv回调
        public delegate void RecvCallback(byte[] buf);
        public RecvCallback recvcallback = null;
        public void setRecvCallback(RecvCallback callback)
        {
            recvcallback = callback;
        }
    }
}
