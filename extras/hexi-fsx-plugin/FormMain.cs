using System;
using System.Timers;
using System.Windows.Forms;
using FSUIPC;

namespace HexiInputsFsx
{
    using SystemTimer = System.Timers.Timer;

    public partial class FormMain : Form
    {
        private static readonly log4net.ILog log = log4net.LogManager.GetLogger
    (System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

        private bool formClosed = false;
        private DateTime fsxLastUiUpdate;
        private DateTime fsxLastFpsUpdate;
        private int fsxOpsSinceLastUpdate = 0;
        private const int fsxFpsCollectInterval = 2000;
        private const int fsxUiUpdateInterval = 1000 / 5;

        StatusMap statusMap;
        FsxController fsxController = new FsxController();
        SystemTimer timerFsxConnect = new SystemTimer();
        SystemTimer timerHexiConnect = new SystemTimer();

        public FormMain()
        {
            InitializeComponent();
            ListViewHelper.EnableDoubleBuffer(listView);

            fsxController.FsxiConnected += FsxController_FsxiConnected;
            fsxController.FsxiDisconnected += FsxController_FsxiDisconnected;
            fsxController.FsxiValueBagUpdated += FsxController_FsxiValueBagUpdated;

            statusMap = new StatusMap(this.listView);

            timerFsxConnect.Interval = 1000;
            timerFsxConnect.Elapsed += TimerFsxConnect_Elapsed;

            timerHexiConnect.Interval = 1000;
            timerHexiConnect.Elapsed += TimerHexiConnect_Elapsed;
        }

        private void FsxController_FsxiValueBagUpdated(object sender, EventArgs e)
        {
            fsxOpsSinceLastUpdate++;
            
            if (DateTime.Now.Subtract(fsxLastUiUpdate).TotalMilliseconds > fsxUiUpdateInterval)
            {
                statusMap.Sync(fsxController.ValueBag);
                fsxLastUiUpdate = DateTime.Now;
            }

            if (DateTime.Now.Subtract(fsxLastFpsUpdate).TotalMilliseconds > fsxFpsCollectInterval)
            {
                statusMap[StatusMapTypes.FSX_REFRESH_RATE] = fsxOpsSinceLastUpdate / (fsxFpsCollectInterval / 1000.0d);
                statusMap.Sync(fsxController.ValueBag);
                fsxLastFpsUpdate = DateTime.Now;
                fsxOpsSinceLastUpdate = 0;
            }
            
        }

        private void FsxController_FsxiDisconnected(object sender, EventArgs e)
        {
            log.Debug("Fsx FSUIPC disconnected");
            if (!formClosed)
            {
                timerFsxConnect.Start();
            }
        }

        private void FsxController_FsxiConnected(object sender, EventArgs e)
        {
            log.Debug("Fsx FSUIPC connected");
            timerFsxConnect.Stop();
        }
        
        private void TimerHexiConnect_Elapsed(object sender, ElapsedEventArgs e)
        {
            
        }

        private void TimerFsxConnect_Elapsed(object sender, ElapsedEventArgs e)
        {
            log.Debug("Trying to connect to Fsx FSUIPC");
            fsxController.Connect();
        }

        private void FormMain_Load(object sender, EventArgs e)
        {
            timerFsxConnect.Start();
            timerHexiConnect.Start();
        }

        private void FormMain_FormClosed(object sender, FormClosedEventArgs e)
        {
            fsxController.Disconnect();
        }

        private void FormMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            timerFsxConnect.Stop();
            timerHexiConnect.Stop();
            formClosed = true;
        }
    }
}
