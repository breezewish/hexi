from sanic.response import json
from hexi.service import event
from hexi.service import plugin
from hexi.plugin.BaseCoreModule import BaseCoreModule


class BaseManager(BaseCoreModule):
  """
  Implements plugin activate & deactivate logic
  """

  def __init__(self, id, plugin_category, plugin_class):
    super().__init__(id)
    self.plugin_category = plugin_category
    self.plugin_class = plugin_class
    self.config_default['enabled_plugins'] = []

  def init(self):
    super().init()

    @self.bp.route('/api/plugins')
    async def get_plugins(request):
      raw_plugins = plugin.get_plugins_in_category(self.plugin_category)
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
          'enabled': self._get_current_activated_plugins(),
        },
      })

    @self.bp.route('/api/plugins/enabled', methods=['POST'])
    async def set_activated_plugins(request):
      activated_plugins = request.json['id']
      plugin.set_activated_plugins(self.plugin_category, activated_plugins)
      self.config['enabled_plugins'] = self._get_current_activated_plugins()
      self.save_config()
      return json({
        'code': 200,
        'data': activated_plugins,
      })

    event.subscribe(self._activate_plugins, ['hexi.start'])
    plugin.add_category(self.plugin_category, self.plugin_class)

  def _get_current_activated_plugins(self):
    raw_plugins = plugin.get_plugins_in_category(self.plugin_category)
    return [raw_plugin.details.get('Core', 'Id')
            for raw_plugin in raw_plugins
            if raw_plugin.plugin_object.is_activated]

  async def _activate_plugins(self, e):
    plugin.set_activated_plugins(self.plugin_category, self.config['enabled_plugins'])
