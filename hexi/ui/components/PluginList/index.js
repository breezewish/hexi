import PluginList from './PluginList';
import PluginListItem from './PluginListItem';

export default {
  install(Vue) {
    Vue.component(PluginList.name, PluginList);
    Vue.component(PluginListItem.name, PluginListItem);
  },
};
