import PLUGIN_MANIFEST from '../fsx.plugin';
import _ from 'lodash';

class PluginInputFsx {
  registerRoutes(routes) {
    routes.push({
      name: 'inputPluginFsxConfig',
      parent: 'hexiInputManagerConfigActivatedPlugin',
      path: `/plugins/${PLUGIN_MANIFEST.Core.Id}/config`,
      component: require('./PluginConfig.vue'),
      meta: {
        title: '配置 FSX 插件',
      },
    });
  }
}

Hexi.registerPlugin(PluginInputFsx);
