import logging
import json
import os
import configparser
import asyncio

from sanic import Blueprint
from sanic.response import text
from yapsy.PluginManager import PluginManager
from hexi.service import web

_logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()
pm = PluginManager()
plugins_by_id = {}
plugins_by_category = {}
plugins_filter = {}

bp = Blueprint('plugin', url_prefix='/core/plugin')


@bp.route('/loadPlugins.js')
async def get_plugins(request):
  pids = [plugin.details.get('Core', 'Id')
    for plugin in pm.getAllPlugins()]
  resp_text = 'var EXTERNAL_PLUGINS = {0};\n'.format(json.dumps(pids));
  for id in pids:
    resp_text += ('try{{document.write(\'<script src="/plugins/{0}/static/main.js"></script>\');}}catch(e){{}}\n'.format(id))
  return text(resp_text, content_type='application/javascript')


def init():
  web.app.blueprint(bp)
  pm.setPluginPlaces(['./plugins'])
  pm.setPluginInfoExtension('plugin')

def load():
  pm.setCategoriesFilter(plugins_filter)
  pm.collectPlugins()
  for plugin in pm.getAllPlugins():
    try:
      id = plugin.details.get('Core', 'Id')
    except configparser.NoOptionError:
      _logger.error('Plugin `{0}` is ignored because of missing valid `Id` property.'.format(plugin.name))
    try:
      category = plugin.details.get('Core', 'Category')
      assert(category in plugins_by_category.keys())
    except configparser.NoOptionError:
      _logger.error('Plugin `{0}` is ignored because of missing valid `Category` property.'.format(plugin.name))

    plugins_by_category[category].append(plugin)
    plugins_by_id[id] = plugin

    # assign static directories
    bp = Blueprint('plugin-{0}'.format(id), url_prefix='/plugins/{0}'.format(id))
    bp.static('/static', os.path.join(os.path.dirname(plugin.path), '.ui_built'))
    plugin.plugin_object.id = id;
    plugin.plugin_object.category = category;
    plugin.plugin_object.bp = bp;
    plugin.plugin_object.load()
    web.app.blueprint(bp)

def add_category(category, PluginType):
  plugins_filter[category] = PluginType
  plugins_by_category[category] = []

def get_plugins_in_category(category):
  return plugins_by_category[category]

def set_activated_plugins(category, ids):
  plugins = get_plugins_in_category(category)
  for plugin in plugins:
    id = plugin.details.get('Core', 'Id')
    if id in ids:
      activate_plugin_by_id(id)
    else:
      deactivate_plugin_by_id(id)

def activate_plugin_by_id(id):
  if not plugins_by_id[id].plugin_object.is_activated:
    _logger.info('Plugin {0} activated'.format(id))
    plugins_by_id[id].plugin_object.activate()

def deactivate_plugin_by_id(id):
  if plugins_by_id[id].plugin_object.is_activated:
    _logger.info('Plugin {0} deactivated'.format(id))
    plugins_by_id[id].plugin_object.deactivate()
