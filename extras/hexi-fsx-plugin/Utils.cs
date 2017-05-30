using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HexiInputsFsx
{
    public static class Utils
    {
        private static DateTime utcDate = new DateTime(1970, 1, 1);

        public static Int32 GetTimeStamp(DateTime dt)
        {
            return (Int32)dt.Subtract(utcDate).TotalSeconds;
        }
    }
}
