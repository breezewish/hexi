const loadedPlugins = [];

export default async function loadPlugin(PluginClass) {
  const plugin = new PluginClass();
  if (plugin.init) {
    await plugin.init();
  }
  if (plugin.registerRoutes) {
    await plugin.registerRoutes(Hexi.routerBuilder.getRawData());
  }
  if (plugin.registerSidebarMenus) {
    await plugin.registerSidebarMenus(Hexi.sidebarBuilder.getRawData());
  }
  loadedPlugins.push(plugin);
}
