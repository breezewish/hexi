<template>
  <ui-section-container key="page_input-manager">
    <ui-section title="输入信号" width="300px">
      <ui-section-content extend>
        <ui-menu-list>
          <ui-menu-list-item :href="{ name: 'hexiInputManagerConfigActivatedPlugin' }">
            <i class="fa fa-signal" aria-hidden="true"></i> 输入信号源
          </ui-menu-list-item>
          <ui-menu-list-item :href="'/abc'">
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
  name: 'page_input-manager_config',
}
</script>
