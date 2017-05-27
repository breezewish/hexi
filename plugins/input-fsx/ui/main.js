import PLUGIN_MANIFEST from '../fsx.plugin';
import _ from 'lodash';

class PluginInputFsx {
  constructor() {
    console.log(PLUGIN_MANIFEST);
  }

  registerRoutes(routes) {
    routes.push({
      name: 'fsxPluginConfigPage',
      parent: 'hexiInputManagerConfigPage',
      path: '/plugins/input-fsx/config',
      component: require('./PluginConfig.vue'),
      meta: {
        title: '配置 FSX 插件',
      },
    });
  }
}

Hexi.registerPlugin(PluginInputFsx);
