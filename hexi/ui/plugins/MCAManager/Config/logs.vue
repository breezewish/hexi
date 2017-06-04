<template>
  <ui-section-container key="page-mca-manager-config-logs" v-loading.body="loading">
    <ui-section title="信号调试" width="500px">
      <ui-section-content>
        <ui-chart-line v-for="cd in chartData" ref="chart" :width="480" :height="150" :chart-data="cd" :options="chartOptions"></ui-chart-line>
      </ui-section-content>
    </ui-section>
  </ui-section-container>
</template>

<script>
// TODO: refine together with InputManager

import colors from '@core/utils/colors';
import RollingArray from '@core/utils/rollingArray';
import moment from 'moment';
import _ from 'lodash';

const COLUMNS = ['labels', 'Transform X', 'Transform Y', 'Transform Z', 'Rotate Alpha', 'Rotate Beta', 'Rotate Gamma'];
const COLORS = Object.keys(colors);

let ws;
let rawData = _(COLUMNS)
  .map(key => [key, new RollingArray(400)])
  .fromPairs()
  .value();

function buildChartData() {
  const ret = [];
  COLUMNS.slice(1).forEach((key, idx) => {
    ret.push({
      labels: rawData[COLUMNS[0]].get(),
      datasets: [
        {
          label: key,
          lineTension: 0,
          borderColor: colors[COLORS[idx]],
          borderWidth: 1,
          backgroundColor: colors[COLORS[idx]],
          fill: false,
          data: rawData[key].get()
        }
      ],
    })
  });
  return ret;
}

export default {
  name: 'page-mca-manager-config-logs',
  data() {
    return {
      chartData: buildChartData(),
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
        responsive: false,
        maintainAspectRatio: false,
      },
      ws: null,
      loading: false,
    };
  },
  created() {
    this.loading = true;
    ws = new WebSocket(`ws://${location.host}/core/mca/api/mca_log`);
    ws.addEventListener('open', () => {
      this.loading = false;
    });
    ws.addEventListener('message', ev => {
      try {
        const data = JSON.parse(ev.data);
        console.log(data);
        data.forEach(row => {
          rawData[COLUMNS[0]].pushWithoutResize(moment(row[0] * 1000).format('mm:ss'));
          COLUMNS.slice(1).forEach((key, idx) => {
            rawData[key].pushWithoutResize(row[1][idx]);
          });
        });
        COLUMNS.forEach(key => rawData[key].resize());
        COLUMNS.slice(1).forEach((key, idx) => this.$refs.chart[idx]._chart.update(0));
      } catch (e) {
      }
    });
  },
  destroyed() {
    ws.close();
  },
}
</script>
