<template>
  <div class="section" :style="{ width: this.width }">
    <div class="section_inner">
      <div class="section_title">{{ this.title }}</div>
      <div class="section_body"><slot></slot></div>
    </div>
  </div>
</template>

<script>
import './section.styl';

export default {
  name: 'ui-section',
  props: {
    title: {
      type: String,
      required: true,
    },
    width: {
      type: String,
      default: '100%',
    },
  },
}
</script>
