export default class UiLayoutPage {
  static id = 'UiLayoutPage';
  registerRoutes(routes) {
    routes['hexiLayoutPage'] = {
      path: '/',
      component: require('./Layout.vue'),
      children: [],
      meta: {
        title: 'Hexi',
      },
    };
  }
}
