export default class UiLayoutPage {
  registerRoutes(routes) {
    routes.push({
      name: 'hexiLayoutPage',
      path: '/',
      component: require('./Layout.vue'),
      meta: {
        title: 'Hexi',
      },
    });
  }
}
