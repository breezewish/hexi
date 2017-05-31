<template>
  <ui-section-container key="page-input-fsx-plugin-config">
    <ui-section title="FSX 插件" width="300px">
      <ui-section-content extend>
        <ui-menu-list>
          <ui-menu-list-item :href="{ name: 'inputPluginFsxConfigDataOptions' }">
            <i class="fa fa-cog" aria-hidden="true"></i> 数据监听配置
          </ui-menu-list-item>
          <ui-menu-list-item :href="'/abc'">
            <i class="fa fa-info-circle" aria-hidden="true"></i> 数据接收日志
          </ui-menu-list-item>
        </ui-menu-list>
      </ui-section-content>
    </ui-section>
    <transition name="transition-page" mode="out-in">
      <router-view></router-view>
    </transition>
  </ui-section-container>
</template>

<script>
export default {
  name: 'page-input-fsx-plugin-config',
}
</script>
