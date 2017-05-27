<template>
  <li :class="[
    'plugin-list_item',
    {
      'can-check': canCheck,
      'is-checked': canCheck && checked,
    }
  ]" @click="handleClick">
    <div class="plugin-list_item_title">{{ item.name }}</div>
    <div class="plugin-list_item_description" v-if="item.description">
      <p>{{ item.description }}</p>
    </div>
    <div class="plugin-list_item_actions" v-if="showConfigure || canCheck">
      <el-button
        type="text"
        @click.stop="handleClickConfigure"
        :disabled="!item.configurable"
        v-if="showConfigure"
      >配置</el-button>
      <el-button
        type="text"
        @click.stop="handleClickChoose"
        :disabled="checked"
        v-if="canCheck"
      >
        <span v-if="checked">已选择</span>
        <span v-if="!checked">选择</span>
      </el-button>
    </div>
    <div class="plugin-list_item_check" v-if="canCheck && checked"><i class="el-icon-check"></i></div>
  </li>
</template>

<script>
export default {
  name: 'ui-plugin-list-item',
  props: {
    item: {
      type: Object,
      default() {
        return {};
      },
    },
    canCheck: {
      type: Boolean,
      default: true,
    },
    checked: {
      type: Boolean,
      default: false,
    },
    showConfigure: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleClick() {
      if (this.canCheck) {
        this.$emit('click', !this.checked);
      }
    },
    handleClickChoose() {
      this.handleClick();
    },
    handleClickConfigure() {
      this.$router.push(`/plugins/${this.item.id}/config`);
    },
  },
}
</script>

<style scoped lang="stylus">
.plugin-list_item
  user-select: none
  position: relative
  display: block
  padding: 10px
  border-top: 1px solid oc-gray-3
  border-bottom: 1px solid oc-gray-3
  margin-bottom: -1px
  color: #666
  transition: background .1s linear

  &.can-check
    cursor: pointer
    padding-right: 30px

    &:hover
      background: oc-gray-1

.plugin-list_item_title
  margin-bottom: 5px

.plugin-list_item_description
  margin: 10px 0
  margin-bottom: 5px
  font-size: 12px
  color: oc-gray-6

.plugin-list_item_check
  position: absolute
  right: 10px
  top: 50%
  margin-top: -7px
  color: oc-green-5

</style>
