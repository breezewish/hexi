import PLUGIN_MANIFEST from '@module/../manifest.plugin';
import _ from 'lodash';

class Plugin {
  registerRoutes(routes) {
    routes.push({
      name: 'inputPluginFlightAttitudeMain',
      parent: 'hexiInputManagerConfigActivatedPlugin',
      path: `/plugins/${PLUGIN_MANIFEST.Core.Id}/config`,
      component: require('./main.vue'),
      meta: {
        title: '标准飞行姿态插件',
      },
    });
  }
}

Hexi.registerPlugin(Plugin);
