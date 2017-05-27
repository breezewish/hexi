import Vue from 'vue';
import Router from 'vue-router';

import buildTreeFromPlain from '@core/utils/buildTree';

export default class RouterBuilder {
  constructor() {
    this.router = null;
    this.plain = [];
  }

  getRawData() {
    return this.plain;
  }

  buildRouter() {
    if (this.router) {
      return this.router;
    }
    const routes = buildTreeFromPlain(this.plain);
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
