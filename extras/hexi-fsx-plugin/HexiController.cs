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

        public static int ListenPort = 16315;
        
        public HexiValueBag ValueBag { get; private set; } = new HexiValueBag();
        
        private Thread serverThread;
        private CancellationTokenSource serverCancelTokenSource;

        private static void ThreadFunc(Object obj)
        {
            HexiController controller = (HexiController)obj;
            controller.RunServer().Wait();
        }

        public void Start()
        {
            if (ValueBag.ServerStarted)
            {
                return;
            }
            serverThread = new Thread(new ParameterizedThreadStart(ThreadFunc));
            serverThread.Start(this);
            ValueBag.ServerStarted = true;
            log.Info("Hexi Server Listener started");
        }

        public void Stop()
        {
            if (!ValueBag.ServerStarted)
            {
                return;
            }
            StopServer();
            serverThread.Abort();
            serverThread = null;
            ValueBag.ServerStarted = false;
            log.Info("Hexi Server Listener stopped");
        }

        private static ManualResetEvent allDone = new ManualResetEvent(false);

        private async Task RunServer()
        {
            serverCancelTokenSource = new CancellationTokenSource();
            TcpListener listener = new TcpListener(new IPAddress(new byte[] { 0, 0, 0, 0 }), ListenPort);
            listener.Start();
            try
            {
                while (true)
                {
                    try
                    {
                        TcpClient tcpClient = await Task.Run(() => listener.AcceptTcpClientAsync(), serverCancelTokenSource.Token);
                        HandleTcpClientConnectionAsync(tcpClient, serverCancelTokenSource.Token);
                    }
                    catch (OperationCanceledException)
                    {
                        throw;
                    }
                    catch (Exception ex)
                    {
                        log.Error(ex);
                    }
                }
            }
            catch (OperationCanceledException)
            {
            }
        }

        private void StopServer()
        {
            serverCancelTokenSource.Cancel();
        }

        private async void HandleTcpClientConnectionAsync(TcpClient tcpClient, CancellationToken token)
        {
            Console.WriteLine("Remote connection from {0}", tcpClient.Client.RemoteEndPoint.ToString());

            HexiUdpClient client = new HexiUdpClient(((IPEndPoint)tcpClient.Client.RemoteEndPoint).Address.MapToIPv4().ToString());

            ValueBag.HexiClientCount++;
            using (await ValueBag.HexiClientsLock.WriterLockAsync())
            {
                ValueBag.HexiClients.Add(client);
            }

            try
            {
                var bufferReqSize = new byte[4];
                byte[] bufferReqBody;
                byte[] bufferResSize;
                byte[] bufferResBody;
                NetworkStream networkStream = tcpClient.GetStream();

                while (true)
                {
                    // Read size
                    await networkStream.ReadAsync(bufferReqSize, 0, 4, token);
                    Int32 reqSize = BitConverter.ToInt32(bufferReqSize, 0);

                    // Read body
                    bufferReqBody = new byte[reqSize];
                    await networkStream.ReadAsync(bufferReqBody, 0, reqSize);
                    TcpRequestMessage request = TcpRequestMessage.Parser.ParseFrom(bufferReqBody);

                    bool responseSuccess = false;
                    switch (request.MsgType)
                    {
                        case TcpRequestMessage.Types.MsgType.Ping:
                            responseSuccess = true;
                            break;
                        case TcpRequestMessage.Types.MsgType.SetConfig:
                            client.SetTransmissionTarget(request.SetConfigBody.UdpPort, request.SetConfigBody.UdpToken);
                            responseSuccess = true;
                            break;
                        case TcpRequestMessage.Types.MsgType.TestConnection:
                            responseSuccess = true;
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
                    await networkStream.WriteAsync(bufferResSize, 0, 4, token);
                    await networkStream.WriteAsync(bufferResBody, 0, bufferResBody.Length, token);
                }
            }
            catch (OperationCanceledException)
            {
                throw;
            }
            catch (Exception)
            {
            }
            finally
            {
                if (tcpClient.Connected)
                {
                    tcpClient.Close();
                }
                client.Close();
                ValueBag.HexiClientCount--;
                using (await ValueBag.HexiClientsLock.WriterLockAsync())
                {
                    ValueBag.HexiClients.Remove(client);
                }
            }
        }

        public void BroadcastFsxData(FsxValueBag valueBag)
        {
            UdpResponseMessage msg = new UdpResponseMessage
            {
                MsgType = UdpResponseMessage.Types.MsgType.TransmissionData,
                TransmissionDataBody = new UdpResponseMessage.Types.TransmissionDataBody
                {
                    XAcceleration = valueBag.XAcceleration,
                    YAcceleration = valueBag.YAcceleration,
                    ZAcceleration = valueBag.ZAcceleration,
                    PitchVelocity = valueBag.PitchVelocity,
                    RollVelocity = valueBag.RollVelocity,
                    YawVelocity = valueBag.YawVelocity,
                },
            };
            using (ValueBag.HexiClientsLock.WriterLock())
            {
                foreach (var client in ValueBag.HexiClients)
                {
                    if (client.Valid)
                    {
                        client.SendMessage(msg);
                    }
                }
            }
        }
    }
}
