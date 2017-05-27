<template>
  <transition name="transition-page" mode="out-in">
    <router-view></router-view>
  </transition>
</template>

<script>
export default {
  name: 'app',
}
</script>

<style lang="stylus">
html, body, .vcContainer
  height: 100%

.transition-page
  &-enter-active, &-leave-active
    will-change: opacity
    transition: opacity .2s
    transition-timing-function: ease-out-cubic
  &-enter, &-leave-active
    opacity: 0

.transition-highlight
  &-enter-active, &-leave-active
    will-change: background-color, opacity
    transition: background-color .5s, opacity .5s
    transition-timing-function: linear
  &-enter
    background-color: rgba(green, 0.5)
  &-enter-active
    background-color: none
  &-leave-active
    opacity: 0

.el-menu-item, .el-submenu__title
  line-height: 40px
  height: @line-height

.ui-mono
  textarea, input
    font-family: Menlo,Monaco,Consolas,Courier,monospace

.el-textarea__inner
  font-size: 12px
</style>
