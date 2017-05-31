import * as THREE from 'three';

export default class Leg {
  /**
   * options.p1
   * options.p2
   * options.radius
   */
  constructor(options) {
    this.options = options;
    this.createGeometry();
    this.createObject();
  }

  createGeometry() {
    this.geometry = new THREE.TubeGeometry(
      new THREE.LineCurve3(this.options.p1, this.options.p2),
      1,
      this.options.radius,
      4
    );
  }

  updateEndpoints(p1, p2) {
    this.options.p1 = p1;
    this.options.p2 = p2;
    this.updateGeometry();
  }

  updateGeometry() {
    if (this.geometry) {
      this.geometry.dispose();
      this.geometry = null;
    }
    this.createGeometry();
    this.object.geometry = this.geometry;
  }

  createObject() {
    const material = new THREE.MeshNormalMaterial();

    this.object = new THREE.Mesh(this.geometry, material);
    this.object.castShadow = true;
    this.object.receiveShadow = true;
  }

  addTo(layer) {
    layer.add(this.object);
  }

}
