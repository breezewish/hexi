import store from '@core/store';

import buildTreeFromPlain from '@core/utils/buildTree';

export default class SidebarBuilder {
  constructor() {
    this.plain = [];
  }
  getRawData() {
    return this.plain;
  }
  updateStore() {
    const menus = buildTreeFromPlain(this.plain);
    store.commit('layout/setMenu', menus);
  }
}
