<template>
  <div class="vcContainer">
    <div class="layoutLeft">
      <el-menu
        class="leftMenu"
        theme="dark"
        :default-active="$route.fullPath"
        :default-openeds="['problem_manage', 'answer_manage', 'user']"
        router
      >
        <component key="menu.index" v-for="menu in sidebarMenus" :is="getMenuType(menu)" :index="menu.index">
          <span v-if="!menu.hasChildren">{{ menu.title }}</span>
          <template slot="title" v-if="menu.hasChildren">{{ menu.title }}</template>
          <el-menu-item key="submenu.index" v-for="submenu in menu.children" :index="submenu.index">{{ submenu.title }}</el-menu-item>
        </component>
        <!--<el-menu-item index="/">仪表盘</el-menu-item>
        <el-submenu index="problem_manage" v-if="['admin', 'ta'].indexOf(session.role) > -1">
          <template slot="title">作业</template>
          <el-menu-item index="/manage/assignments">所有作业</el-menu-item>
          <el-menu-item index="/manage/assignments/create">创建作业</el-menu-item>
        </el-submenu>
        <el-submenu index="user">
          <template slot="title">用户 ({{ session.username }})</template>
          <el-menu-item index="/user/change-password">修改密码</el-menu-item>
          <el-menu-item index="/user/logout">登出</el-menu-item>
        </el-submenu>-->
      </el-menu>
    </div>
    <div class="layoutMain">
      <transition name="transition-page" mode="out-in">
        <router-view></router-view>
      </transition>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'layout',
  computed: {
    ...mapState('layout', [
      'sidebarMenus',
    ]),
  },
  methods: {
    getMenuType(menuItem) {
      if (menuItem.hasChildren) {
        return 'el-submenu';
      } else {
        return 'el-menu-item';
      }
    },
    handleSelect(index) {
      this.$router.push(index);
    },
  },
}
</script>

<style scoped lang="stylus">
.vcContainer
  width: 100%
  height: 100%
  overflow: hidden
  position: relative

.layoutLeft, .layoutMain
  position: absolute

.layoutLeft
  left: 0
  top: 0
  width: 120px
  height: 100%

.layoutMain
  left: 120px
  top: 0
  right: 0
  height: 100%
  background: oc-gray-1
  overflow-x: auto
  white-space: nowrap
  font-size: 0

.leftMenu
  height: 100%
</style>
