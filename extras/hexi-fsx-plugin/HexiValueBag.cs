using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HexiInputsFsx
{
    public class HexiValueBag
    {
        public bool ServerStarted { get; set; }
        public bool HexiConnected { get; set; }
        public string HexiHost { get; set; }
        public int HexiPort { get; set; }

        public HexiValueBag()
        {
            Clear();
        }

        public void Clear()
        {
            ServerStarted = false;
            HexiConnected = false;
            HexiHost = null;
            HexiPort = 0;
        }
    }
}
