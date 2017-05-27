<template>
  <ui-section-container key="page-input-config" v-loading.body="loading">
    <ui-section title="配置 FSX 插件" width="300px">
      <ui-section-content>
        Hello World
      </ui-section-content>
    </ui-section>
  </ui-section-container>
</template>

<script>
import API from '@core/utils/api';

export default {
  name: 'page-input-fsx-plugin-config',
  data() {
    return {
      data: {},
      loading: false,
    };
  },
  created() {
    this.initData();
  },
  watch: {
    $route: 'initData',
  },
  methods: {
    async initData() {
      // TODO
    },
  },
}
</script>
