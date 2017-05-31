import PLUGIN_MANIFEST from '@module/../manifest.plugin';
import _ from 'lodash';

class Plugin {
  registerRoutes(routes) {
    routes.push({
      name: 'outputPluginStewartVisualizeConfig',
      parent: 'hexiOutputManagerConfigActivatedPlugin',
      path: `/plugins/${PLUGIN_MANIFEST.Core.Id}/config`,
      component: require('./config/index.vue'),
      meta: {
        title: '六自由度平台可视化仿真',
      },
    });
  }
}

Hexi.registerPlugin(Plugin);
