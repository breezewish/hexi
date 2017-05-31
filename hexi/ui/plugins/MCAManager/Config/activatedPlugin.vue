<template>
  <ui-section-container key="page-mca-manager-config-activated-plugin" v-loading.body="loading">
    <ui-section title="选择体感模拟算法" width="300px">
      <ui-section-content>
        以下是当前已安装的体感模拟算法，请选择一项。
      </ui-section-content>
      <ui-section-content>
        <el-button type="primary" :disabled="!hasChanged || loading" @click="handleSave">保存</el-button>
      </ui-section-content>
      <ui-section-content extend>
        <ui-plugin-list
          :data="data.available"
          :canCheck="true"
          :canMultiCheck="false"
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
  name: 'page-mca-manager-config-activated-plugin',
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
  watch: {
    $route: 'initData',
  },
  methods: {
    async initData() {
      this.loading = true;
      this.checkedId = [];
      try {
        this.data = (await API.enabledPlugins.get('mca')).data;
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
        API.enabledPlugins.set('mca', this.checkedId);
        this.hasChanged = false;
      } finally {
        this.loading = false;
      }
    },
  },
}
</script>
