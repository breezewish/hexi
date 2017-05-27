from sanic import Blueprint
from sanic.response import json
from hexi.service import event
from hexi.service import plugin
from hexi.service import web
from hexi.plugin.InputPlugin import InputPlugin

bp = Blueprint('input', url_prefix='/input')


@bp.route('/api/plugins')
async def webGetPlugins(request):
  raw_plugins = plugin.getPluginsInCategory('input')
  plugins = [{
    'id': raw_plugin.details.get('Core', 'Id'),
    'name': raw_plugin.name,
    'description': raw_plugin.description,
    'configurable': raw_plugin.plugin_object.configurable,
  } for raw_plugin in raw_plugins]
  return json({
    'available': plugins,
    'enabled': [raw_plugin.details.get('Core', 'Id')
      for raw_plugin in raw_plugins
      if raw_plugin.plugin_object.is_activated],
  })


@bp.route('/api/plugins/enabled', methods=['POST'])
async def webSetEnabledPlugins(request):
  activated_plugins = request.json['id']
  plugin.setActivatedPlugins('input', activated_plugins)
  return json(activated_plugins)


def init():
  web.app.blueprint(bp)
  plugin.addCategory('input', InputPlugin)
