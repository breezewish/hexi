import logging
import json
import os

from sanic import Blueprint
from sanic.response import text
from yapsy.PluginManager import PluginManager
from hexi.service import web

_logger = logging.getLogger(__name__)

pm = PluginManager()
pluginsById = {}
pluginsByCategory = {}
pluginsFilter = {}

bp = Blueprint('plugin', url_prefix='/core/plugin')


@bp.route('/loadPlugins.js')
async def webGetPlugins(request):
  pluginIdList = [plugin.details.get('Core', 'Id')
    for plugin in pm.getAllPlugins()]
  responseText = 'var EXTERNAL_PLUGINS = {0};\n'.format(json.dumps(pluginIdList));
  for id in pluginIdList:
    responseText += ('try{{document.write(\'<script src="/plugins/{0}/static/main.js"></script>\');}}catch(e){{}}\n'.format(id))
  return text(responseText, content_type='application/javascript')


def init():
  web.app.blueprint(bp)
  pm.setPluginPlaces(['./plugins'])
  pm.setPluginInfoExtension('plugin')

def load():
  pm.setCategoriesFilter(pluginsFilter)
  pm.collectPlugins()
  for plugin in pm.getAllPlugins():
    try:
      id = plugin.details.get('Core', 'Id')
    except ConfigParser.NoOptionError:
      _logger.error('Plugin `{0}` is ignored because of missing valid `Id` property.'.format(plugin.name))
    try:
      category = plugin.details.get('Core', 'Category')
      assert(category in pluginsByCategory.keys())
    except ConfigParser.NoOptionError:
      _logger.error('Plugin `{0}` is ignored because of missing valid `Category` property.'.format(plugin.name))

    pluginsByCategory[category].append(plugin)
    pluginsById[id] = plugin

    # assign static directories
    bp = Blueprint('plugin-{0}'.format(id), url_prefix='/plugins/{0}'.format(id))
    bp.static('/static', os.path.join(os.path.dirname(plugin.path), '.ui_built'))
    web.app.blueprint(bp)
    plugin.plugin_object.bp = bp;
    plugin.plugin_object.load()

def addCategory(category, PluginType):
  pluginsFilter[category] = PluginType
  pluginsByCategory[category] = []

def getPluginsInCategory(category):
  return pluginsByCategory[category]

def setActivatedPlugins(category, ids):
  plugins = getPluginsInCategory(category)
  for plugin in plugins:
    id = plugin.details.get('Core', 'Id')
    if id in ids:
      activatePluginById(id)
    else:
      deactivatePluginById(id)

def activatePluginById(id):
  if not pluginsById[id].plugin_object.is_activated:
    pluginsById[id].plugin_object.activate()

def deactivatePluginById(id):
  if pluginsById[id].plugin_object.is_activated:
    pluginsById[id].plugin_object.deactivate()
