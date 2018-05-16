using System;
using System.Threading;
using System.Text;
using System.Runtime.InteropServices;

namespace SocketClient
{
    class Program
    {
        static Client m_client = new Client();

        static void Main(string[] args)
        {
            //目前还是简单的同步架构
            m_client.start();
        }
    }
}
