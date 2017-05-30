using Nito.AsyncEx;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

namespace HexiInputsFsx
{
    public class HexiValueBag
    {
        public bool ServerStarted { get; set; }
        public int HexiClientCount { get; set; }
        public List<HexiUdpClient> HexiClients { get; set; }
        public AsyncReaderWriterLock HexiClientsLock = new AsyncReaderWriterLock();

        public HexiValueBag()
        {
            Clear();
        }

        public void Clear()
        {
            ServerStarted = false;
            HexiClientCount = 0;
            HexiClients = new List<HexiUdpClient>();
        }

        public static string HexiClientsToString(object addresses, AsyncReaderWriterLock locker)
        {
            if (addresses == null)
            {
                return "";
            }
            using (locker.ReaderLock())
            {
                var addr = (List<HexiUdpClient>)addresses;
                return String.Join(", ", addr);
            }
        }
    }
}
