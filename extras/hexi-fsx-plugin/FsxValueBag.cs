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
        public double PitchVelocity { get; set; } // in degree/sec2
        public double RollVelocity { get; set; }
        public double YawVelocity { get; set; }

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
            PitchVelocity = 0.0d;
            RollVelocity = 0.0d;
            YawVelocity = 0.0d;
        }
    }
}
