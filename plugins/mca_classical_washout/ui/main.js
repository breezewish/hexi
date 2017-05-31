import PLUGIN_MANIFEST from '@module/../manifest.plugin';
import _ from 'lodash';

class Plugin {
  registerRoutes(routes) {
    routes.push({
      name: 'mcaPluginClassicalWashoutConfig',
      parent: 'hexiMCAManagerConfigActivatedPlugin',
      path: `/plugins/${PLUGIN_MANIFEST.Core.Id}/config`,
      component: require('./config/index.vue'),
      meta: {
        title: '经典洗出体感模拟',
      },
    });
    routes.push({
      name: 'mcaPluginClassicalWashoutConfigScale',
      parent: 'mcaPluginClassicalWashoutConfig',
      path: `/plugins/${PLUGIN_MANIFEST.Core.Id}/config/scale`,
      component: require('./config/scale.vue'),
      meta: {
        title: '信号缩放策略',
      },
    });
    routes.push({
      name: 'mcaPluginClassicalWashoutConfigScaleRange',
      parent: 'mcaPluginClassicalWashoutConfig',
      path: `/plugins/${PLUGIN_MANIFEST.Core.Id}/config/scaleRange`,
      component: require('./config/scaleRange.vue'),
      meta: {
        title: '信号缩放范围',
      },
    });
  }
}

Hexi.registerPlugin(Plugin);
