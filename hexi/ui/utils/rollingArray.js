export default class RollingArray {
  constructor(maxSize) {
    this.maxSize = maxSize;
    this.internal = [];
  }

  get() {
    return this.internal;
  }

  push(item) {
    this.internal.push(item);
    this.resize();
  }

  pushBucket(items) {
    items.forEach(item => this.internal.push(item));
    this.resize();
  }

  pushWithoutResize(item) {
    this.internal.push(item);
  }

  resize() {
    const l = this.internal.length;
    if (l > this.maxSize) {
      this.internal.splice(0, l - this.maxSize);
    }
  }
}
