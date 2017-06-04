<template>
  <ui-section-container key="page-input-fsx-plugin-config-logs" v-loading.body="loading">
    <ui-section title="数据接收日志" width="300px">
      <ui-section-content>
        <ui-chart-line ref="chart" :chart-data="chartData" :options="chartOptions"></ui-chart-line>
      </ui-section-content>
    </ui-section>
  </ui-section-container>
</template>

<script>
import API from '@module/api';
import colors from '@core/utils/colors';
import moment from 'moment';

let ws;
let rawData = {
  'labels': [],
  'receive': [],
  'drop': [],
};

function pushWithLimit(array, data, maxLength = 100) {
  array.push(data);
  const l = array.length;
  if (l > maxLength) {
    array.splice(0, l - maxLength);
  }
}

export default {
  name: 'page-input-fsx-plugin-config-logs',
  computed() {

  },
  data() {
    return {
      chartData: {
        labels: rawData.labels,
        datasets: [
          {
            label: '接收 UDP 包',
            lineTension: 0,
            borderColor: colors.blue,
            borderWidth: 1,
            backgroundColor: colors.blue,
            fill: false,
            data: rawData.receive
          },
          {
            label: '丢弃 UDP 包',
            lineTension: 0,
            borderColor: colors.red,
            borderWidth: 1,
            backgroundColor: colors.red,
            fill: false,
            data: rawData.drop
          },
        ]
      },
      chartOptions: {
        scales: {
          xAxes: [{
            gridLines: {
              display: true
            },
          }],
          yAxes: [{
            gridLines: {
              display: true
            },
          }],
        },
        elements: {
          point: { radius: 0 }
        },
      },
      ws: null,
      loading: false,
    };
  },
  created() {
    this.loading = true;
    ws = new WebSocket(`ws://${location.host}/plugins/input_fsx/api/udp_log`);
    ws.addEventListener('open', () => {
      this.loading = false;
    });
    ws.addEventListener('message', ev => {
      try {
        const data = JSON.parse(ev.data);
        data.forEach(row => {
          pushWithLimit(rawData.labels, moment(row[0] * 1000).format('mm:ss'));
          pushWithLimit(rawData.receive, row[1]);
          pushWithLimit(rawData.drop, row[2]);
        });
        console.log(rawData.labels.length);
        this.$refs.chart._chart.update(0);
      } catch (e) {
      }
    });
  },
  destroyed() {
    ws.close();
  },
}
</script>
