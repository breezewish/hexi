using System;
using System.Threading;

using FSUIPC;

namespace HexiInputsFsx
{
    public class FsxController
    {
        private static readonly log4net.ILog log = log4net.LogManager.GetLogger
    (System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        public event EventHandler FsxiConnected;
        public event EventHandler FsxiDisconnected;
        public event EventHandler FsxiValueBagUpdated;
        public FsxValueBag ValueBag { get; private set; } = new FsxValueBag();

        private Thread updateThread;
        public static int UpdateInterval { get; } = 1000 / 20;

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
        private Offset<Double> ipcPitchVelocity = new Offset<Double>(0x30A8);
        private Offset<Double> ipcRollVelocity = new Offset<Double>(0x30B0);
        private Offset<Double> ipcYawVelocity = new Offset<Double>(0x30B8);

        private static void ThreadFunc(Object obj)
        {
            FsxController controller = (FsxController)obj;
            DateTime beginTime, endTime;
            double elapsedMs;
            while (true)
            {
                beginTime = DateTime.Now;
                controller.threadTick();
                endTime = DateTime.Now;
                elapsedMs = (endTime - beginTime).TotalMilliseconds;
                if (elapsedMs < UpdateInterval && elapsedMs >= 0)
                {
                    Thread.Sleep(UpdateInterval - (int)elapsedMs);
                }
            }
        }

        private void threadTick()
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
                ValueBag.PitchVelocity = ipcPitchVelocity.Value * 180d / Math.PI;
                ValueBag.RollVelocity = ipcRollVelocity.Value * 180d / Math.PI;
                ValueBag.YawVelocity = ipcYawVelocity.Value * 180d / Math.PI;
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

                updateThread = new Thread(new ParameterizedThreadStart(ThreadFunc));
                updateThread.Start(this);
                return true;
            }
            catch (FSUIPCException)
            {
                return false;
            }
            catch (Exception e)
            {
                log.Error(e);
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
                updateThread.Abort();
                updateThread = null;
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
