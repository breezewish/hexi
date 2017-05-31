export default class UiOutputManagerPlugin {
  registerRoutes(routes) {
    routes.push({
      name: 'hexiOutputManagerConfig',
      parent: 'hexiLayoutPage',
      path: '/core/outputManager/config',
      component: require('./Config/index.vue'),
      meta: {
        title: '输出信号',
      },
    });
  }

  registerSidebarMenus(menus) {
    menus.push({
      name: 'hexiOutputManagerConfig',
      index: '/core/outputManager/config',
      title: '输出信号',
    });
  }
}
