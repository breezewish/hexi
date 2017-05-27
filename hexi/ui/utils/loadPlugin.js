const loadedPlugins = {};

export default async function loadPlugin(PluginClass) {
  if (PluginClass.id == undefined) {
    throw new Error(`Expect class ${PluginClass.name} to have 'id'`);
  }
  if (loadedPlugins[PluginClass.id]) {
    return;
  }
  const plugin = new PluginClass();
  loadedPlugins[PluginClass.id] = plugin;
  if (plugin.init) {
    await plugin.init();
  }
  if (plugin.registerRoutes) {
    await plugin.registerRoutes(Hexi.routerBuilder.namedRoutes);
  }
  if (plugin.registerSidebarMenus) {
    await plugin.registerSidebarMenus(Hexi.sidebarBuilder.menus);
  }
}
