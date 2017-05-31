<template>
  <ui-section-container key="page-mca-classical-washout-config">
    <ui-section title="经典洗出体感模拟" width="300px">
      <ui-section-content extend>
        <ui-menu-list>
          <ui-menu-list-item :href="{ name: 'mcaPluginClassicalWashoutConfigScale' }">
            <i class="fa fa-cog" aria-hidden="true"></i> 信号缩放配置
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
  name: 'page-mca-classical-washout-config',
}
</script>
