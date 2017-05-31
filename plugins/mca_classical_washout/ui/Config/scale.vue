<template>
  <ui-section-container key="page-mca-classical-washout-config-scale" v-loading.body="loading">
    <ui-section title="信号缩放" width="300px">
      <ui-section-content>
        <el-form ref="form" :model="data" label-position="top">
          <el-form-item key="type" label="缩放器类型">
             <el-select v-model="data.type" placeholder="请选择缩放器" style="width: 100%">
              <el-option label="三次缩放器" value="third-order"></el-option>
              <el-option label="线性缩放器" value="linear"></el-option>
            </el-select>
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
  name: 'page-mca-classical-washout-config-scale',
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
      this.loading = true;
      try {
        this.data = (await API.config.scale.get()).data;
      } finally {
        this.loading = false;
      }
    },
    async submit() {
      await API.config.scale.set(this.data);
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
