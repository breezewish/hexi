<template>
  <ui-section-container key="page-mca-classical-washout-config-scale-range" v-loading.body="loading">
    <ui-section title="信号缩放范围" width="300px">
      <ui-section-content>
        <p>以下范围由实际数据测定。</p>
      </ui-section-content>
      <ui-section-content>
        <el-table :data="tableData" style="width: 100%">
          <el-table-column
            prop="key"
            label="数据名"
            width="180">
          </el-table-column>
          <el-table-column
            prop="value"
            label="最大值">
          </el-table-column>
        </el-table>
       </ui-section-content>
       <ui-section-content>
        <div>
          <el-button @click="update()">刷新</el-button>
          <el-button @click="resetZero()">归零</el-button>
        </div>
      </ui-section-content>
    </ui-section>
  </ui-section-container>
</template>

<script>
import API from '@module/api';
import _ from 'lodash';

const keyMap = {
  x: '前后加速度',
  y: '左右加速度',
  z: '垂直加速度',
  alpha: '横滚速度',
  beta: '俯仰速度',
  gamma: '偏航速度',
}

export default {
  name: 'page-mca-classical-washout-config-scale-range',
  data() {
    return {
      tableData: [],
      loading: false,
    };
  },
  created() {
    this.initData();
  },
  methods: {
    async initData() {
      this.loading = true;
      try {
        this.data = (await API.config.scale.get()).data;
        this.tableData = _(this.data.src_max)
          .toPairs()
          .map(([key, value]) => ({key: keyMap[key], value: value}))
          .value()
      } finally {
        this.loading = false;
      }
    },
  },
}
</script>
