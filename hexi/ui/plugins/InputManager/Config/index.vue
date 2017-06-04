<template>
  <ui-section-container key="page-input-manager-config">
    <ui-section title="输入信号" width="300px">
      <ui-section-content extend>
        <ui-menu-list>
          <ui-menu-list-item :href="{ name: 'hexiInputManagerConfigActivatedPlugin' }">
            <i class="fa fa-paper-plane" aria-hidden="true"></i> 输入信号源
          </ui-menu-list-item>
          <ui-menu-list-item :href="{ name: 'hexiInputManagerConfigLogs' }">
            <i class="fa fa-bug" aria-hidden="true"></i> 信号调试
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
  name: 'page-input-manager-config',
}
</script>
