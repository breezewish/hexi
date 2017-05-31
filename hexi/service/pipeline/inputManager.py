import collections

from sanic import Blueprint
from sanic.response import json
from hexi.service import event
from hexi.service import plugin
from hexi.service import web
from hexi.plugin.InputPlugin import InputPlugin

data_log_queue = collections.deque(maxlen=500)
bp = Blueprint('input', url_prefix='/core/input')


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
    'code': 200,
    'data': {
      'available': plugins,
      'enabled': [raw_plugin.details.get('Core', 'Id')
        for raw_plugin in raw_plugins
        if raw_plugin.plugin_object.is_activated],
    },
  })


@bp.route('/api/plugins/enabled', methods=['POST'])
async def webSetEnabledPlugins(request):
  activated_plugins = request.json['id']
  plugin.setActivatedPlugins('input', activated_plugins)
  return json({
    'code': 200,
    'data': activated_plugins,
  })


def on_pipeline_input_data(e):
  print(e)


def init():
  web.app.blueprint(bp)
  event.subscribe(on_pipeline_input_data, ['hexi.pipeline.input.data'])
  plugin.addCategory('input', InputPlugin)
