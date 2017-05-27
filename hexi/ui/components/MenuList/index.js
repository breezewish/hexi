import MenuList from './MenuList';
import MenuListItem from './MenuListItem';

export default {
  install(Vue) {
    Vue.component(MenuList.name, MenuList);
    Vue.component(MenuListItem.name, MenuListItem);
  },
};
