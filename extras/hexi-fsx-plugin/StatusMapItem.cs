using Nito.AsyncEx;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;

namespace HexiInputsFsx
{
    public class StatusMapItem
    {
        private static Func<object, AsyncReaderWriterLock, string> DefaultValueToString = (obj, locker) =>
        {
            // lock ignored
            return obj.ToString();
        };

        public static Func<object, AsyncReaderWriterLock, string> DoubleValueToString = (obj, locker) =>
        {
            // lock ignored
            double val = (double)obj;
            return String.Format("{0:+0.000;-0.000}", val);
        };
        
        public StatusMapTypes Id { get; set; }
        public string DisplayName { get; set; }
        public string Hint { get; set; }
        public object Value { get; set; }
        public AsyncReaderWriterLock ValueLocker { get; set; } = null;
        public Func<object, AsyncReaderWriterLock, string> ValueToString { get; set; }

        public StatusMapItem()
        {
            ValueToString = DefaultValueToString;
        }
    }
}
