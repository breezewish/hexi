using System;
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace HexiInputsFsx
{
    public enum StatusMapTypes
    {
        FSX_CONNECTED,
        HEXI_CONNECTED,
        FSX_REFRESH_RATE,
        FSX_PAUSED,
        FSX_AIR_SPEED,
        FSX_LAT,
        FSX_LNG,
        FSX_X_VEL,   // Sway (Lateral)
        FSX_Y_VEL,   // Heave (Vertical)
        FSX_Z_VEL,   // Surge (Longitudinal)
        FSX_X_ACC,
        FSX_Y_ACC,
        FSX_Z_ACC,
        FSX_PITCH_VEL,
        FSX_ROLL_VEL,
        FSX_YAW_VEL,
    }

    public class StatusMap
    {
        private Dictionary<StatusMapTypes, StatusMapItem> map = new Dictionary<StatusMapTypes, StatusMapItem>();
        private Dictionary<StatusMapTypes, ListViewItem> liMap = new Dictionary<StatusMapTypes, ListViewItem>();
        private ListView listView;

        private void AddProperty(StatusMapItem item)
        {
            map.Add(item.Id, item);

            var li = new ListViewItem(item.DisplayName);
            li.SubItems.Add(item.ValueToString(item.Value));
            li.SubItems.Add(item.Hint);
            listView.Items.Add(li);
            liMap.Add(item.Id, li);
        }

        public StatusMap(ListView lv)
        {
            listView = lv;

            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_CONNECTED,
                DisplayName = "Fsx Connected",
                Value = false,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.HEXI_CONNECTED,
                DisplayName = "Hexi Connected",
                Value = false,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_REFRESH_RATE,
                DisplayName = "Fsx Refresh Rate (ops/sec)",
                Value = 0.0d,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_PAUSED,
                DisplayName = "Fsx Paused",
                Value = true,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_AIR_SPEED,
                DisplayName = "Object Real Air Speed",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_LAT,
                DisplayName = "Object Latitude (degree)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_LNG,
                DisplayName = "Object Longitude (degree)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_X_VEL,
                DisplayName = "X (Lateral) Velocity (ft/sec)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_Y_VEL,
                DisplayName = "Y (Vertical) Velocity (ft/sec)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_Z_VEL,
                DisplayName = "Z (Longitudinal) Velocity (ft/sec)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_X_ACC,
                DisplayName = "X (Lateral) Acceleration (ft/sec2)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_Y_ACC,
                DisplayName = "Y (Vertical) Acceleration (ft/sec2)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_Z_ACC,
                DisplayName = "Z (Longitudinal) Acceleration (ft/sec2)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_PITCH_VEL,
                DisplayName = "Pitch Velocity (degree/sec)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_ROLL_VEL,
                DisplayName = "Roll Velocity (degree/sec)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
            AddProperty(new StatusMapItem
            {
                Id = StatusMapTypes.FSX_YAW_VEL,
                DisplayName = "Yaw Velocity (degree/sec)",
                Value = 0.0d,
                ValueToString = StatusMapItem.DoubleValueToString,
            });
        }

        private void SetValue(StatusMapTypes id, object value)
        {
            if (!map.ContainsKey(id))
            {
                throw new InvalidOperationException();
            }
            map[id].Value = value;
        }

        private object GetValue(StatusMapTypes id)
        {
            if (!map.ContainsKey(id))
            {
                throw new InvalidOperationException();
            }
            return map[id].Value;
        }

        private string GetDisplayValue(StatusMapTypes id)
        {
            if (!map.ContainsKey(id))
            {
                throw new InvalidOperationException();
            }
            var item = map[id];
            return item.ValueToString(item.Value);
        }

        public object this[StatusMapTypes id]
        {
            get
            {
                return GetValue(id);
            }
            set
            {
                SetValue(id, value);
            }
        }

        public void RenderItem(StatusMapTypes id)
        {
            listView.Invoke((MethodInvoker)delegate
            {
                listView.BeginUpdate();

                string displayValue = GetDisplayValue(id);
                liMap[id].SubItems[1].Text = displayValue;

                listView.EndUpdate();
            });
        }

        public void RenderAllItems()
        {
            listView.Invoke((MethodInvoker)delegate
            {
                listView.BeginUpdate();

                foreach (var id in map.Keys)
                {
                    string displayValue = GetDisplayValue(id);
                    liMap[id].SubItems[1].Text = displayValue;
                }

                listView.EndUpdate();
            });
        }

        public void Sync(FsxValueBag fsxValueBag)
        {
            SetValue(StatusMapTypes.FSX_CONNECTED, fsxValueBag.Connected);
            SetValue(StatusMapTypes.FSX_PAUSED, fsxValueBag.Paused);
            SetValue(StatusMapTypes.FSX_AIR_SPEED, fsxValueBag.TrueAirSpeed);
            SetValue(StatusMapTypes.FSX_LAT, fsxValueBag.Lat);
            SetValue(StatusMapTypes.FSX_LNG, fsxValueBag.Lng);
            SetValue(StatusMapTypes.FSX_X_VEL, fsxValueBag.XVelocity);
            SetValue(StatusMapTypes.FSX_Y_VEL, fsxValueBag.YVelocity);
            SetValue(StatusMapTypes.FSX_Z_VEL, fsxValueBag.ZVelocity);
            SetValue(StatusMapTypes.FSX_X_ACC, fsxValueBag.XAcceleration);
            SetValue(StatusMapTypes.FSX_Y_ACC, fsxValueBag.YAcceleration);
            SetValue(StatusMapTypes.FSX_Z_ACC, fsxValueBag.ZAcceleration);
            SetValue(StatusMapTypes.FSX_PITCH_VEL, fsxValueBag.PitchVelocity);
            SetValue(StatusMapTypes.FSX_ROLL_VEL, fsxValueBag.RollVelocity);
            SetValue(StatusMapTypes.FSX_YAW_VEL, fsxValueBag.YawVelocity);
            RenderAllItems();
        }
    }
}
