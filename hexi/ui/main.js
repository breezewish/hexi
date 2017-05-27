import 'element-ui/lib/theme-default/reset.css';
import 'element-ui/lib/theme-default/index.css';

import Vue from 'vue';
import Router from 'vue-router';
import ElementUI from 'element-ui';
import Moment from 'vue-moment';
import UiSection from '@core/components/Section';
import UiPluginList from '@core/components/PluginList';
import App from '@core/App';
import store from '@core/store';
import SidebarBuilder from '@core/utils/sidebarBuilder';
import RouterBuilder from '@core/utils/routerBuilder';

Vue.use(Router);
Vue.use(ElementUI);
Vue.use(Moment);
Vue.use(UiSection);
Vue.use(UiPluginList);

const Hexi = {};
window.Hexi = Hexi;

Hexi.routerBuilder = new RouterBuilder();
Hexi.sidebarBuilder = new SidebarBuilder();
Hexi.loadPlugin = require('@core/utils/loadPlugin').default;

async function main() {
  await Hexi.loadPlugin(require('@core/plugins/LayoutPage').default);
  await Hexi.loadPlugin(require('@core/plugins/NotFoundPage').default);
  await Hexi.loadPlugin(require('@core/plugins/InputManagerConfigPage').default);

  const router = Hexi.routerBuilder.buildRouter();
  Hexi.sidebarBuilder.updateStore();

  new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App),
  });
}

main().catch(e => console.error(e));
