import _ from 'lodash';

export default function buildTreeFromPlain(list, idField = 'name', orderField = 'order', parentField = 'parent') {
  const sortedList = _(list)
    .map((item, idx) => {
      item[orderField] = item[orderField] || 0;
      item.__index = idx;
      return item;
    })
    .sortBy([orderField, '__index'])
    .map(item => {
      delete item[orderField];
      delete item.__index;
      return item;
    })
    .value();

  const mapping = _.keyBy(sortedList, idField);
  const root = [];

  sortedList.forEach(item => {
    const parentId = item[parentField];
    if (parentId) {
      const parent = mapping[parentId];
      if (parent) {
        parent.children = parent.children || [];
        parent.children.push(item);
      }
    } else {
      root.push(item);
    }
  });

  sortedList.forEach(item => {
    delete item[parentField];
  });

  return root;
}
