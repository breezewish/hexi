<template>
  <ui-section-container key="page-output-manager-config-activated-plugin" v-loading.body="loading">
    <ui-section title="选择目标体感平台" width="300px">
      <ui-section-content>
        以下是当前已安装的体感平台驱动，您可以选择多个作为体感信号输出目标。
      </ui-section-content>
      <ui-section-content>
        <el-button type="primary" :disabled="!hasChanged || loading" @click="handleSave">保存</el-button>
      </ui-section-content>
      <ui-section-content extend>
        <ui-plugin-list
          :data="data.available"
          :canCheck="true"
          :canMultiCheck="true"
          :checkedId="checkedId"
          :showConfigure="true"
          @change="handleChange"
        ></ui-plugin-list>
      </ui-section-content>
    </ui-section>
    <transition name="transition-page" mode="out-in">
      <router-view></router-view>
    </transition>
  </ui-section-container>
</template>

<script>
import API from '@core/utils/api';

export default {
  name: 'page-output-manager-config-activated-plugin',
  data() {
    return {
      data: {},
      loading: false,
      hasChanged: false,
    };
  },
  created() {
    this.initData();
  },
  methods: {
    async initData() {
      this.loading = true;
      this.checkedId = [];
      try {
        this.data = (await API.enabledPlugins.get('output')).data;
        this.checkedId = this.data.enabled;
      } finally {
        this.loading = false;
      }
    },
    handleChange(newCheckedId) {
      this.hasChanged = true;
      this.checkedId = [...newCheckedId];
      this.$forceUpdate();
    },
    async handleSave() {
      this.loading = true;
      try {
        API.enabledPlugins.set('output', this.checkedId);
        this.hasChanged = false;
      } finally {
        this.loading = false;
      }
    },
  },
}
</script>
