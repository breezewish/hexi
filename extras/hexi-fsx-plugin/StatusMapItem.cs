using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace HexiInputsFsx
{
    public class StatusMapItem
    {
        private static Func<object, string> DefaultValueToString = (obj) =>
        {
            return obj.ToString();
        };

        public static Func<object, string> DoubleValueToString = (obj) =>
        {
            double val = (double)obj;
            return String.Format("{0:+0.000;-0.000}", val);
        };

        public StatusMapTypes Id { get; set; }
        public string DisplayName { get; set; }
        public string Hint { get; set; }
        public object Value { get; set; }
        public Func<object, string> ValueToString { get; set; }

        public StatusMapItem()
        {
            ValueToString = DefaultValueToString;
        }
    }
}
