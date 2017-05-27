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
        title: '输入信号源',
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
