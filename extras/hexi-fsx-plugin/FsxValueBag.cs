using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace HexiInputsFsx
{
    public class FsxValueBag
    {
        public bool Connected { get; set; }
        public bool Paused { get; set; }
        public double TrueAirSpeed { get; set; } // in knots
        public double Lat { get; set; } // in degree
        public double Lng { get; set; }
        public double XVelocity { get; set; } // in ft/sec
        public double YVelocity { get; set; }
        public double ZVelocity { get; set; }
        public double XAcceleration { get; set; } // in ft/sec2
        public double YAcceleration { get; set; }
        public double ZAcceleration { get; set; }
        public double Pitch { get; set; } // in degree
        public double Bank { get; set; }
        public double Heading { get; set; }
        public double PitchAcceleration { get; set; } // in degree/sec2
        public double RollAcceleration { get; set; }
        public double YawAcceleration { get; set; }

        public FsxValueBag()
        {
            Clear();
        }

        public void Clear()
        {
            Connected = false;
            Paused = false;
            TrueAirSpeed = 0.0d;
            Lat = 0.0d;
            Lng = 0.0d;
            XVelocity = 0.0d;
            YVelocity = 0.0d;
            ZVelocity = 0.0d;
            XAcceleration = 0.0d;
            YAcceleration = 0.0d;
            ZAcceleration = 0.0d;
            Pitch = 0.0d;
            Bank = 0.0d;
            Heading = 0.0d;
            PitchAcceleration = 0.0d;
            RollAcceleration = 0.0d;
            YawAcceleration = 0.0d;
        }
    }
}
