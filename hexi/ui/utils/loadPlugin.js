const loadedPlugins = [];

export default async function loadPlugin(PluginClass) {
  const plugin = new PluginClass();
  if (plugin.init) {
    await plugin.init();
  }
  if (plugin.registerRoutes) {
    await plugin.registerRoutes(Hexi.routerBuilder.namedRoutes);
  }
  if (plugin.registerSidebarMenus) {
    await plugin.registerSidebarMenus(Hexi.sidebarBuilder.menus);
  }
  loadedPlugins.push(plugin);
}
