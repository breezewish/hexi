import collections

from sanic.response import json
from hexi.service import event
from hexi.service import plugin
from hexi.plugin.BaseCoreModule import BaseCoreModule
from hexi.plugin.InputPlugin import InputPlugin

data_log_queue = collections.deque(maxlen=500)


class InputManager(BaseCoreModule):
  def __init__(self):
    super().__init__('input')
    self.config_default = {
      'enabled_plugins': []
    }

  def init(self):
    super().init()

    @self.bp.route('/api/plugins')
    async def webGetPlugins(request):
      raw_plugins = plugin.getPluginsInCategory('input')
      plugins = [{
        'id': raw_plugin.details.get('Core', 'Id'),
        'name': raw_plugin.name,
        'description': raw_plugin.description,
        'configurable': raw_plugin.plugin_object.configurable,
      } for raw_plugin in raw_plugins]
      return json({
        'code': 200,
        'data': {
          'available': plugins,
          'enabled': self.get_real_enabled_plugins(),
        },
      })

    @self.bp.route('/api/plugins/enabled', methods=['POST'])
    async def webSetEnabledPlugins(request):
      activated_plugins = request.json['id']
      plugin.setActivatedPlugins('input', activated_plugins)
      self.config['enabled_plugins'] = self.get_real_enabled_plugins()
      self.save_config()
      return json({
        'code': 200,
        'data': activated_plugins,
      })

    event.subscribe(self.on_pipeline_input_data, ['hexi.pipeline.input.data'])
    plugin.addCategory('input', InputPlugin)

  def get_real_enabled_plugins(self):
    raw_plugins = plugin.getPluginsInCategory('input')
    return [raw_plugin.details.get('Core', 'Id')
            for raw_plugin in raw_plugins
            if raw_plugin.plugin_object.is_activated]

  def on_pipeline_input_data(self, e):
    print(e)
