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
import RollingArray from '@core/utils/rollingArray';

let ws;
let rawData = {
  'labels': new RollingArray(100),
  'receive': new RollingArray(100),
  'drop': new RollingArray(100),
};

export default {
  name: 'page-input-fsx-plugin-config-logs',
  data() {
    return {
      chartData: {
        labels: rawData.labels.get(),
        datasets: [
          {
            label: '接收 UDP 包',
            lineTension: 0,
            borderColor: colors.blue,
            borderWidth: 1,
            backgroundColor: colors.blue,
            fill: false,
            data: rawData.receive.get()
          },
          {
            label: '丢弃 UDP 包',
            lineTension: 0,
            borderColor: colors.red,
            borderWidth: 1,
            backgroundColor: colors.red,
            fill: false,
            data: rawData.drop.get()
          },
        ],
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
          point: { radius: 0 },
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
          rawData.labels.pushWithoutResize(moment(row[0] * 1000).format('mm:ss'));
          rawData.receive.pushWithoutResize(row[1]);
          rawData.drop.pushWithoutResize(row[2]);
        });
        rawData.labels.resize();
        rawData.receive.resize();
        rawData.drop.resize();
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
