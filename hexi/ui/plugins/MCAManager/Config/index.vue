<template>
  <ui-section-container key="page-mca-manager-config">
    <ui-section title="体感模拟" width="300px">
      <ui-section-content extend>
        <ui-menu-list>
          <ui-menu-list-item :href="{ name: 'hexiMCAManagerConfigActivatedPlugin' }">
            <i class="fa fa-code" aria-hidden="true"></i> 体感模拟算法
          </ui-menu-list-item>
          <ui-menu-list-item :href="{ name: 'hexiMCAManagerConfigLogs' }">
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
import API from '@core/utils/api';

export default {
  name: 'page-mca-manager-config',
}
</script>
