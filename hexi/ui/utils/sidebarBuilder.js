import store from '@core/store';

function buildMenus(node) {
  const menus = _(node)
    .map((rawMenu, name) => {
      const menu = {
        order: 0,
        ...rawMenu,
      };
      if (menu.children) {
        menu.children = buildMenus(menu.children);
      }
      menu.hasChildren = menu.children && menu.children.length > 0;
      return menu;
    })
    .orderBy(['order'], ['asc'])
    .map(menu => {
      delete menu.order;
      return menu;
    })
    .value();

  return menus;
}

export default class SidebarBuilder {
  constructor() {
    this.menus = {};
  }
  updateStore() {
    const menus = buildMenus(this.menus);
    store.commit('layout/setMenu', menus);
  }
}
