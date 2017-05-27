import logging

from yapsy.PluginManager import PluginManager
from hexi.plugin.McaPlugin import McaPlugin
from hexi.plugin.InputPlugin import InputPlugin
from hexi.plugin.OutputPlugin import OutputPlugin

_logger = logging.getLogger(__name__)
pm = PluginManager()
pluginsById = {}
pluginsByCategory = {}
pluginsFilter = {}


def init():
  pm.setPluginPlaces(['./plugins'])
  pm.setPluginInfoExtension('plugin')

def load():
  pm.setCategoriesFilter(pluginsFilter)
  pm.collectPlugins()
  for plugin in pm.getAllPlugins():
    try:
      id = plugin.details.get('Core', 'Id')
      category = plugin.details.get('Core', 'Category')
      assert(category in pluginsByCategory.keys())
      pluginsByCategory[category].append(plugin)
      pluginsById[id] = plugin
    except:
      _logger.error('Plugin `{0}` is ignored because of missing valid `Id` or `Category` property.'.format(plugin.name))

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
