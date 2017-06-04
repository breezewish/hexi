export default class UiInputManagerPlugin {
  registerRoutes(routes) {
    routes.push({
      name: 'hexiInputManagerConfig',
      parent: 'hexiLayoutPage',
      path: '/core/inputManager/config',
      component: require('./Config/index.vue'),
      meta: {
        title: '输入信号',
      },
    });
    routes.push({
      name: 'hexiInputManagerConfigActivatedPlugin',
      parent: 'hexiInputManagerConfig',
      path: '/core/inputManager/config/activatedPlugin',
      component: require('./Config/activatedPlugin.vue'),
      meta: {
        title: '选择输入信号源',
      },
    });
    routes.push({
      name: 'hexiInputManagerConfigLogs',
      parent: 'hexiInputManagerConfig',
      path: '/core/inputManager/config/logs',
      component: require('./Config/logs.vue'),
      meta: {
        title: '信号调试',
      },
    });
  }

  registerSidebarMenus(menus) {
    menus.push({
      name: 'hexiInputManagerConfig',
      index: '/core/inputManager/config',
      title: '输入信号',
    });
  }
}
