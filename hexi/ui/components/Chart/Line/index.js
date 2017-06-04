import { Line } from 'vue-chartjs';

const Component = Line.extend({
  props: ['options', 'chartData'],
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
});

export default {
  install(Vue) {
    Vue.component('ui-chart-line', Component);
  },
};
