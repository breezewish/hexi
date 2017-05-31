using System;
using System.Timers;
using System.Windows.Forms;
using FSUIPC;
using System.Threading.Tasks;

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
        HexiController hexiController = new HexiController();
        SystemTimer timerHexiStatusUpdate = new SystemTimer();
        SystemTimer timerFsxConnect = new SystemTimer();

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

            timerHexiStatusUpdate.Interval = 1000;
            timerHexiStatusUpdate.Elapsed += TimerHexiStatusUpdate_Elapsed;

            hexiController.Start();
            this.Text += String.Format(" (Listen: {0})", HexiController.ListenPort);
        }

        private void TimerHexiStatusUpdate_Elapsed(object sender, ElapsedEventArgs e)
        {
            statusMap.Sync(hexiController.ValueBag);
        }
        
        private void FsxController_FsxiValueBagUpdated(object sender, EventArgs e)
        {
            fsxOpsSinceLastUpdate++;
            if (!fsxController.ValueBag.Paused)
            {
                hexiController.BroadcastFsxData(fsxController.ValueBag);
            }
            
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
        
        private void TimerFsxConnect_Elapsed(object sender, ElapsedEventArgs e)
        {
            log.Debug("Trying to connect to Fsx FSUIPC");
            fsxController.Connect();
        }

        private void FormMain_Load(object sender, EventArgs e)
        {
            timerFsxConnect.Start();
            timerHexiStatusUpdate.Start();
        }

        private void FormMain_FormClosed(object sender, FormClosedEventArgs e)
        {
            fsxController.Disconnect();
        }

        private void FormMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            hexiController.Stop();
            timerFsxConnect.Stop();
            timerHexiStatusUpdate.Stop();
            formClosed = true;
        }
    }
}
