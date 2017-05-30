using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using FsxProtocol;
using Google.Protobuf;

namespace HexiInputsFsx
{
    public class HexiController
    {
        private static readonly log4net.ILog log = log4net.LogManager.GetLogger
    (System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        public static int ListenPort = 16314;

        public event EventHandler HexiConnected;
        public event EventHandler HexiDisconnected;
        public event EventHandler HexiValueBagUpdated;
        public HexiValueBag ValueBag { get; private set; } = new HexiValueBag();

        public void Start()
        {
            if (ValueBag.ServerStarted)
            {
                return;
            }
        }

        public void Stop()
        {
            if (!ValueBag.ServerStarted)
            {
                return;
            }

        }

        private static ManualResetEvent allDone = new ManualResetEvent(false);

        private async void RunServer()
        {
            TcpListener listener = new TcpListener(new IPAddress(new byte[] { 0, 0, 0, 0 }), ListenPort);
            listener.Start();
            while (true)
            {
                try
                {
                    TcpClient tcpClient = await listener.AcceptTcpClientAsync();
                    HandleTcpClientConnectionAsync(tcpClient);
                }
                catch (Exception ex)
                {
                    log.Error(ex);
                }
            }
        }

        private async void HandleTcpClientConnectionAsync(TcpClient tcpClient)
        {
            Console.WriteLine("Remote connection from {0}", tcpClient.Client.RemoteEndPoint.ToString());
            try
            {
                var bufferReqSize = new byte[4];
                var bufferReqBody = new byte[4096];
                byte[] bufferResSize;
                byte[] bufferResBody;
                NetworkStream networkStream = tcpClient.GetStream();

                while (true)
                {
                    // Read size
                    await networkStream.ReadAsync(bufferReqSize, 0, 4);
                    if (!BitConverter.IsLittleEndian)
                    {
                        Array.Reverse(bufferReqSize);
                    }
                    Int32 reqSize = BitConverter.ToInt32(bufferReqSize, 0);

                    // Read body
                    await networkStream.ReadAsync(bufferReqBody, 0, reqSize);
                    TcpRequestMessage request = TcpRequestMessage.Parser.ParseFrom(bufferReqBody);

                    bool responseSuccess = false;
                    switch (request.MsgType)
                    {
                        case TcpRequestMessage.Types.MsgType.Ping:
                            responseSuccess = true;
                            break;
                        case TcpRequestMessage.Types.MsgType.SetConfig:
                            break;
                        case TcpRequestMessage.Types.MsgType.TestConnection:
                            break;
                    }
                    
                    TcpResponseMessage response = new TcpResponseMessage
                    {
                        Success = responseSuccess,
                        TimeStamp = Utils.GetTimeStamp(DateTime.UtcNow),
                    };

                    // Write size and body
                    bufferResBody = response.ToByteArray();
                    bufferResSize = BitConverter.GetBytes(bufferResBody.Length);
                    await networkStream.WriteAsync(bufferResSize, 0, 4);
                    await networkStream.WriteAsync(bufferResBody, 0, bufferResBody.Length);
                }
            }
            catch (Exception)
            {
                if (tcpClient.Connected)
                {
                    tcpClient.Close();
                }
            }
        }
    }
}
