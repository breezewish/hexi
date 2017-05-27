export default class UiInputManagerConfigPage {
  static id = 'UiInputManagerConfigPage';
  registerRoutes(routes) {
    routes['hexiLayoutPage'].children = routes['hexiLayoutPage'].children || [];
    routes['hexiLayoutPage'].children.push({
      path: '/core/inputConfig',
      component: require('./InputConfig.vue'),
      meta: {
        title: '输入配置',
      },
    });
  }

  registerSidebarMenus(menus) {
    menus['hexiInputConfig'] = {
      index: '/core/inputConfig',
      title: '输入配置',
      children: [],
    };
  }
}
