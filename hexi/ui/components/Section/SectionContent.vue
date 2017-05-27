<template>
  <div :class="[
    'section_content',
    {
      extended: this.extend,
    }
  ]">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'ui-section-content',
  props: {
    extend: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
