<template>
  <ui-section-container key="page-output-manager-config">
    <ui-section title="输出信号" width="300px">
      <ui-section-content extend>
        <ui-menu-list>
          <ui-menu-list-item :href="'/abc'">
            <i class="fa fa-paper-plane" aria-hidden="true"></i> 输出目标
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
  name: 'page-output-manager-config',
}
</script>
