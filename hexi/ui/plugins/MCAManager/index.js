export default class UiMCAManagerPlugin {
  registerRoutes(routes) {
    routes.push({
      name: 'hexiMCAManagerConfig',
      parent: 'hexiLayoutPage',
      path: '/core/mcaManager/config',
      component: require('./Config/index.vue'),
      meta: {
        title: '体感模拟',
      },
    });
    routes.push({
      name: 'hexiMCAManagerConfigActivatedPlugin',
      parent: 'hexiMCAManagerConfig',
      path: '/core/mcaManager/config/activatedPlugin',
      component: require('./Config/activatedPlugin.vue'),
      meta: {
        title: '选择体感模拟算法',
      },
    });
  }

  registerSidebarMenus(menus) {
    menus.push({
      name: 'hexiMCAManagerConfig',
      index: '/core/mcaManager/config',
      title: '体感模拟',
    });
  }
}
