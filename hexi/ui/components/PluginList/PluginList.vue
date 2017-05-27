<template>
  <ul class="plugin-list">
    <ui-plugin-list-item
      v-for="item in sortedData"
      :key="item.id"
      :item="item"
      :canCheck="canCheck"
      :checked="checkedId && checkedId.indexOf(item.id) > -1"
      :showConfigure="showConfigure"
      @click="handleClick(item.id)"
    ></ui-plugin-list-item>
  </ul>
</template>

<script>
import _ from 'lodash';

export default {
  name: 'ui-plugin-list',
  props: {
    data: {
      type: Array,
      default() {
        return [];
      },
    },
    canCheck: {
      type: Boolean,
      default: true,
    },
    canMultiCheck: {
      type: Boolean,
      default: false,
    },
    checkedId: {
      type: Array,
      default() {
        return [];
      },
    },
    showConfigure: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    sortedData() {
      return _.sortBy(this.data, ['id']);
    },
  },
  methods: {
    handleClick(id) {
      let newCheckedId;
      if (this.canMultiCheck) {
        if (this.checkedId.indexOf(id) > -1) {
          newCheckedId = _.difference(this.checkedId, [id]);
        } else {
          newCheckedId = _.union(this.checkedId, [id]);
        }
      } else {
        newCheckedId = [id];
      }
      this.$emit('change', newCheckedId);
    },
  },
}
</script>

<style scoped lang="stylus">

</style>
