import chairModel from '@/models/chair.json';
import * as THREE from 'three';

export default class Chair {
  /**
   * options.material
   */
  constructor(options) {
    this.options = options;
    this.attitude = {
      pitch: 0, // rotateZ
      roll: 0,  // rotateX
      yaw: 0,   // rotateY
      surge: 0, // x
      sway: 0,  // z
      heave: 0, // y
    };
    this.createObject();
  }

  createObject() {
    const loader = new THREE.BufferGeometryLoader();
    const geometry = loader.parse(chairModel);
    geometry.scale(100, 100, 100);
    geometry.rotateY(Math.PI);
    geometry.translate(30, 10, 0);

    this.object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial(this.options.material));
    this.updatePosition();
  }

  updatePosition() {
    this.object.rotation.x = this.attitude.roll;
    this.object.rotation.y = this.attitude.yaw;
    this.object.rotation.z = this.attitude.pitch;
    this.object.position.x = this.attitude.surge;
    this.object.position.y = this.attitude.heave + this.options.yOffset || 0;
    this.object.position.z = this.attitude.sway;
    this.object.updateMatrix();
  }

  addTo(layer) {
    layer.add(this.object);
  }
}
