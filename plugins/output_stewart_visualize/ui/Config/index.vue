<template>
  <ui-section-container key="page-output-stewart-visualize-config">
    <ui-section title="六自由度平台可视化仿真" width="300px">
      <ui-section-content>
        <p><el-button @click="handleClick">打开三维仿真平台</el-button></p>
      </ui-section-content>
    </ui-section>
  </ui-section-container>
</template>

<script>
import PLUGIN_MANIFEST from '@module/../manifest.plugin';

export default {
  name: 'page-output-stewart-visualize-config',
  methods: {
    handleClick() {
      window.open(`/plugins/${PLUGIN_MANIFEST.Core.Id}/static/visualizer/index.html`)
    }
  }
}
</script>
