export default class UiNotFoundPage {
  registerRoutes(routes) {
    routes['hexiNotFound'] = {
      order: -999,
      path: '*',
      component: require('./NotFound.vue'),
      meta: {
        title: '该页未找到',
      },
    };
  }
}
