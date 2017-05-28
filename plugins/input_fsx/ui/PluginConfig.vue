<template>
  <ui-section-container key="page-input-config" v-loading.body="loading">
    <ui-section title="配置 FSX 插件" width="300px">
      <ui-section-content>
        <el-form ref="form" :model="data" label-position="top">
          <el-form-item key="ip" label="FSX 主机 IP 地址">
            <el-input v-model="data.ip"></el-input>
          </el-form-item>
          <el-form-item key="frequency" label="采样周期 (ms)">
            <el-input v-model="data.frequency"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button @click="testConnection()">测试连通性</el-button>
            <el-button @click="submit()">保存</el-button>
            <el-button @click="cancel()">取消</el-button>
          </el-form-item>
        </el-form>
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
      data: {
        ip: '',
        frequency: '10',
      },
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
