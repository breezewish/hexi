<template>
  <ui-section-container key="page-input-fsx-plugin-config-data-options" v-loading.body="loading">
    <ui-section title="数据监听配置" width="300px">
      <ui-section-content>
        <el-form ref="form" :model="data" label-position="top">
          <el-form-item key="tcp_host" label="FSX 主机 IP 地址">
            <el-input v-model="data.tcp_host"></el-input>
          </el-form-item>
          <el-form-item key="tcp_port" label="FSX 主机连接端口">
            <el-input v-model="data.tcp_port"></el-input>
          </el-form-item>
          <el-form-item key="udp_port" label="本地数据端口">
            <el-input v-model="data.udp_port"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button @click="submit()">保存</el-button>
            <el-button @click="cancel()">取消</el-button>
          </el-form-item>
        </el-form>
      </ui-section-content>
    </ui-section>
  </ui-section-container>
</template>

<script>
import API from '@module/api';

export default {
  name: 'page-input-fsx-plugin-config-data-options',
  data() {
    return {
      data: {},
      loading: false,
    };
  },
  created() {
    this.initData();
  },
  methods: {
    async initData() {
      this.loading = true;
      try {
        this.data = (await API.config.get()).data;
      } finally {
        this.loading = false;
      }
    },
    async submit() {
      await API.config.set(this.data);
      this.$notify({
        title: '成功',
        message: '配置更新成功',
        type: 'success'
      });
    },
    cancel() {
      this.$router.go(-1);
    },
  },
}
</script>
