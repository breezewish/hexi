import 'element-ui/lib/theme-default/reset.css';
import 'element-ui/lib/theme-default/index.css';
import 'font-awesome-webpack';

import Vue from 'vue';
import Router from 'vue-router';
import ElementUI from 'element-ui';
import Moment from 'vue-moment';
import UiSection from '@core/components/Section';
import UiPluginList from '@core/components/PluginList';
import UiMenuList from '@core/components/MenuList';
import App from '@core/App';
import store from '@core/store';
import SidebarBuilder from '@core/utils/sidebarBuilder';
import RouterBuilder from '@core/utils/routerBuilder';
import API from '@core/utils/api';

Vue.use(Router);
Vue.use(ElementUI);
Vue.use(Moment);
Vue.use(UiSection);
Vue.use(UiPluginList);
Vue.use(UiMenuList);

const Hexi = {};
window.Hexi = Hexi;

Hexi.routerBuilder = new RouterBuilder();
Hexi.sidebarBuilder = new SidebarBuilder();
Hexi.loadPlugin = require('@core/utils/loadPlugin').default;

Hexi.externalPlugins = [];
Hexi.registerPlugin = (BaseClass) => {
  Hexi.externalPlugins.push(BaseClass);
};

async function main() {
  await Hexi.loadPlugin(require('@core/plugins/LayoutPage').default);
  await Hexi.loadPlugin(require('@core/plugins/NotFoundPage').default);
  await Hexi.loadPlugin(require('@core/plugins/InputManager').default);
  await Promise.all(Hexi.externalPlugins.map(async BaseClass => {
    try {
      Hexi.loadPlugin(BaseClass);
    } catch (e) {
      console.error('Failed to load external plugin: %s', BaseClass.name);
    }
  }));

  const router = Hexi.routerBuilder.buildRouter();
  Hexi.sidebarBuilder.updateStore();

  new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
  });
}

Hexi.start = () => {
  main().catch(e => console.error(e));
};
