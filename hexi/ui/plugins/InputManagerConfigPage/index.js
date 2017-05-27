export default class UiInputManagerConfigPage {
  registerRoutes(routes) {
    routes.push({
      name: 'hexiInputManagerConfigPage',
      parent: 'hexiLayoutPage',
      path: '/core/inputConfig',
      component: require('./InputConfig.vue'),
      meta: {
        title: '输入配置',
      },
    });
  }

  registerSidebarMenus(menus) {
    menus.push({
      name: 'hexiInputConfig',
      index: '/core/inputConfig',
      title: '输入配置',
    });
  }
}
