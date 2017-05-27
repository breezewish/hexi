import Vue from 'vue';

export default {
  namespaced: true,
  state: {
    sidebarMenus: [],
  },
  mutations: {
    setMenu(state, menu) {
      state.sidebarMenus = menu;
    },
  },
}
