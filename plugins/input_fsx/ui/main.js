import PLUGIN_MANIFEST from '../manifest.plugin';
import _ from 'lodash';

class Plugin {
  registerRoutes(routes) {
    routes.push({
      name: 'inputPluginFsxConfig',
      parent: 'hexiInputManagerConfigActivatedPlugin',
      path: `/plugins/${PLUGIN_MANIFEST.Core.Id}/config`,
      component: require('./config/index.vue'),
      meta: {
        title: 'FSX 插件',
      },
    });
    routes.push({
      name: 'inputPluginFsxConfigDataOptions',
      parent: 'inputPluginFsxConfig',
      path: `/plugins/${PLUGIN_MANIFEST.Core.Id}/config/dataOptions`,
      component: require('./config/dataOptions.vue'),
      meta: {
        title: '数据监听配置',
      },
    });
  }
}

Hexi.registerPlugin(Plugin);
