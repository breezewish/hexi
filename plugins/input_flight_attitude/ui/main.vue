<template>
  <ui-section-container key="page-input-fsx-plugin-config" v-loading.body="loading">
    <ui-section title="标准飞行姿态" width="500px">
      <ui-section-content>
        <p>可用姿态：</p>
        <p>
          <el-button
            v-for="state in data.states"
            type="primary"
            :key="state.id"
            :loading="state.id == data.current && data.running"
            :disabled="!state.enabled"
            @click="setState(state.id)"
          >
            {{ state.text }}
            <span v-if="state.id == data.current">(最后姿态)</span>
          </el-button>
        </p>
      </ui-section-content>
      <ui-section-content v-if="data.running">
        <p>当前正在运行姿态：{{ data.current }}</p>
        <p>运行进度：<el-progress :stroke-width="18" :percentage="~~(data.progress * 100)"></el-progress></p>
      </ui-section-content>
    </ui-section>
  </ui-section-container>
</template>

<script>
import API from '@module/api';
import WebSocket from 'reconnecting-websocket';

let ws = null;

export default {
  name: 'page-input-flight-attitude-plugin-main',
  data() {
    return {
      data: {},
      ws: null,
      loading: false,
    };
  },
  created() {
    this.loading = true;
    ws = new WebSocket(`ws://${location.host}/plugins/input_flight_attitude/api/state`);
    ws.addEventListener('open', () => {
      this.loading = false;
    });
    ws.addEventListener('message', ev => {
      try {
        const data = JSON.parse(ev.data);
        this.data = data;
      } catch (e) {
      }
    });
  },
  destroyed() {
    ws.close();
  },
  methods: {
    async setState(stateId) {
      await API.state.set(stateId);
    },
  },
}
</script>
