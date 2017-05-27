<template>
  <ul class="menu-list">
    <slot></slot>
  </ul>
</template>

<script>
export default {
  name: 'ui-menu-list',
}
</script>

<style scoped lang="stylus">
.menu-list
  margin-bottom: 10px
</style>
