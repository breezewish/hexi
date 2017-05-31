<template>
  <li class="menu-list_item">
    <router-link
      class="menu-list_link"
      :to="href"
    >
      <slot></slot>
    </router-link>
  </li>
</template>

<script>
export default {
  name: 'ui-menu-list-item',
  props: {
    href: {
      required: true,
    },
  },
}
</script>

<style lang="stylus">
.menu-list_item
  display: block

.menu-list_link
  user-select: none
  position: relative
  display: block
  padding: 10px
  border-top: 1px solid oc-gray-3
  border-bottom: 1px solid oc-gray-3
  margin-bottom: -1px
  color: #666
  transition: background .1s linear

  .fa
    display: inline-block
    width: 16px
    text-align: center
    margin-right: 5px

  &:hover
    color: #666
    background: oc-gray-1

  &.router-link-active
    background: oc-blue-4
    color: #FFF

</style>
