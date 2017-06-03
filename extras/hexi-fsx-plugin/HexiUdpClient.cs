using FsxProtocol;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using Google.Protobuf;
using Nito.AsyncEx;
using System.Threading;

namespace HexiInputsFsx
{
    public class HexiUdpClient
    {
        private UdpClient client = new UdpClient();
        public string Host { get; private set; }
        public int Port { get; private set; } = 0;
        public bool Valid { get; private set; }
        public int Token { get; set; } = 0;
        public int SerialNumber { get; set; } = 1;

        public HexiUdpClient(String host)
        {
            Host = host;
        }

        public void SetTransmissionTarget(int port, int token)
        {
            Port = port;
            Token = token;
            client.Connect(Host, Port);
            Valid = true;
        }

        public Task<int> SendAsync(byte[] bytes, int n)
        {
            if (Valid)
            {
                return client.SendAsync(bytes, n);
            }
            return Task.FromResult<int>(0);
        }

        public async Task SendMessageAsync(UdpResponseMessage message)
        {
            // No need to add length prefix since packet size < MTU
            SerialNumber = SerialNumber + 1;
            message.Token = Token;
            message.SerialNumber = SerialNumber;
            var body = message.ToByteArray();
            await SendAsync(body, body.Length);
        }

        public void Close()
        {
            Valid = false;
            client.Close();
        }

        public override string ToString()
        {
            return String.Format("{0}:{1} (valid={2},sn={3})", Host, Port, Valid, SerialNumber);
        }

        public void SendMessage(UdpResponseMessage message)
        {
            Task.Run(() => SendMessageAsync(message));
        }
    }
}
