using System;
using System.Timers;
using FSUIPC;

namespace HexiInputsFsx
{
    public class FsxController
    {
        public event EventHandler FsxiConnected;
        public event EventHandler FsxiDisconnected;
        public event EventHandler FsxiValueBagUpdated;
        public int UpdateInterval { get; private set; }
        public FsxValueBag ValueBag { get; private set; } = new FsxValueBag();

        private Timer updateTimer = new Timer();
        private Offset<Int16> ipcPaused = new Offset<Int16>(0x0264);
        private Offset<Int32> ipcTrueAirSpeed = new Offset<Int32>(0x02BC);
        private Offset<Double> ipcLat = new Offset<Double>(0x6010);
        private Offset<Double> ipcLng = new Offset<Double>(0x6018);
        private Offset<Double> ipcXVelocity = new Offset<Double>(0x3098);
        private Offset<Double> ipcYVelocity = new Offset<Double>(0x30A0);
        private Offset<Double> ipcZVelocity = new Offset<Double>(0x3090);
        private Offset<Double> ipcXAcceleration = new Offset<Double>(0x3060);
        private Offset<Double> ipcYAcceleration = new Offset<Double>(0x3068);
        private Offset<Double> ipcZAcceleration = new Offset<Double>(0x3070);
        private Offset<Int32> ipcPitch = new Offset<Int32>(0x0578);
        private Offset<Int32> ipcBank = new Offset<Int32>(0x057C);
        private Offset<Int32> ipcHeading = new Offset<Int32>(0x0580);
        private Offset<Double> ipcPitchAcceleration = new Offset<Double>(0x3078);
        private Offset<Double> ipcRollAcceleration = new Offset<Double>(0x3080);
        private Offset<Double> ipcYawAcceleration = new Offset<Double>(0x3088);

        public FsxController(int _updateInterval)
        {
            UpdateInterval = _updateInterval;
            updateTimer.Interval = _updateInterval;
            updateTimer.Elapsed += UpdateTimer_Elapsed;
        }

        private void UpdateTimer_Elapsed(object sender, ElapsedEventArgs e)
        {
            if (!ValueBag.Connected)
            {
                return;
            }
            try
            {
                FSUIPCConnection.Process();
                ValueBag.Paused = ipcPaused.Value == 1;
                ValueBag.TrueAirSpeed = (double)ipcTrueAirSpeed.Value / 128d;
                ValueBag.Lat = ipcLat.Value;
                ValueBag.Lng = ipcLng.Value;
                ValueBag.XVelocity = ipcXVelocity.Value;
                ValueBag.YVelocity = ipcYVelocity.Value;
                ValueBag.ZVelocity = ipcZVelocity.Value;
                ValueBag.XAcceleration = ipcXAcceleration.Value;
                ValueBag.YAcceleration = ipcYAcceleration.Value;
                ValueBag.ZAcceleration = ipcZAcceleration.Value;
                ValueBag.Pitch = ipcPitch.Value * 360d / (65536d * 65536d);
                ValueBag.Bank = ipcBank.Value * 360d / (65536d * 65536d);
                ValueBag.Heading = ipcHeading.Value * 360d / (65536d * 65536d);
                ValueBag.PitchAcceleration = ipcPitchAcceleration.Value * 180d / Math.PI;
                ValueBag.RollAcceleration = ipcRollAcceleration.Value * 180d / Math.PI;
                ValueBag.YawAcceleration = ipcYawAcceleration.Value * 180d / Math.PI;
                FsxiValueBagUpdated?.Invoke(this, EventArgs.Empty);
            }
            catch (FSUIPCException ex) when (ex.FSUIPCErrorCode == FSUIPCError.FSUIPC_ERR_SENDMSG)
            {
                Disconnect();
            }
            catch (Exception)
            {
                // In case of bad data conversion
            }
        }

        public bool Connect()
        {
            if (ValueBag.Connected)
            {
                return false;
            }
            try
            {
                FSUIPCConnection.Open();
                ValueBag.Clear();
                ValueBag.Connected = true;
                FsxiConnected?.Invoke(this, EventArgs.Empty);
                FsxiValueBagUpdated?.Invoke(this, EventArgs.Empty);
                updateTimer.Start();
                return true;
            }
            catch (FSUIPCException)
            {
                return false;
            }
        }

        public bool Disconnect()
        {
            if (!ValueBag.Connected)
            {
                return false;
            }
            try
            {
                FSUIPCConnection.Close();
                updateTimer.Stop();
                ValueBag.Clear();
                ValueBag.Connected = false;
                FsxiDisconnected?.Invoke(this, EventArgs.Empty);
                FsxiValueBagUpdated?.Invoke(this, EventArgs.Empty);
                return true;
            }
            catch (FSUIPCException)
            {
                return false;
            }
        }
    }
}
