import _ from 'lodash';
import Vue from 'vue';
import Router from 'vue-router';

function buildNamedRoutes(node) {
  const routes = _(node)
    .map((namedRoute, name) => {
      const route = {
        order: 0,
        ...namedRoute,
        name: name,
      };
      if (route.children) {
        route.children = buildNamedRoutes(route.children);
      }
      return route;
    })
    .orderBy(['order'], ['asc'])
    .map(route => {
      delete route.order;
      return route;
    })
    .value();

  return routes;
}

export default class RouterBuilder {
  constructor() {
    this.router = null;
    this.namedRoutes = {};
  }

  buildRouter() {
    if (this.router) {
      return this.router;
    }
    const routes = buildNamedRoutes(this.namedRoutes);
    this.router = new Router({ routes });
    this.router.beforeEach((to, from, next) => {
      if (to.meta.title) {
        document.title = `${to.meta.title} | Hexi`;
      }
      next();
    });
    return this.router;
  }
}
