import * as THREE from 'three';

export default class Plate {
  /**
   * options.radius
   * options.innerRadius
   * options.jointRadius
   * options.alphaDeg
   * options.thickness
   * options.yOffset (default 0)
   * options.reverse (default false)
   */
  constructor(options) {
    this.options = options;
    this.options.alpha = THREE.Math.degToRad(this.options.alphaDeg);
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

  /**
   * options.radius
   * options.alpha
   */
  getPlatePoints(radius, alpha) {
    const shapePoints = [];
    const baseDeg = this.options.reverse ? Math.PI : 0;
    for (let i = 0; i < 3; ++i) {
      const orient = 2 / 3 * Math.PI * i + baseDeg;
      shapePoints.push(new THREE.Vector2(radius * Math.cos(orient - alpha), radius * Math.sin(orient - alpha)));
      shapePoints.push(new THREE.Vector2(radius * Math.cos(orient + alpha), radius * Math.sin(orient + alpha)));
    }
    shapePoints.push(shapePoints[0]);
    return shapePoints;
  }

  createObject() {
    const shape = new THREE.Shape(this.getPlatePoints(this.options.radius, this.options.alpha));
    if (this.options.innerRadius > 0) {
      const inner = new THREE.Path(this.getPlatePoints(this.options.innerRadius, this.options.alpha));
      shape.holes.push(inner);
    }

    const geometry = new THREE.ExtrudeGeometry(shape, {
      amount: this.options.thickness,
      bevelEnabled: false,
    });
    geometry.lookAt(new THREE.Vector3(0, 1, 0));

    const material = new THREE.MeshNormalMaterial();

    this.object = new THREE.Mesh(geometry, material);
    this.object.castShadow = true;
    this.object.receiveShadow = true;

    // A virtual path to calculate joints
    this.jointPoints = this
      .getPlatePoints(this.options.jointRadius, this.options.alpha)
      .slice(0, 6)
      .map(v2 => new THREE.Vector3(v2.x, this.options.thickness / 2, v2.y));
    this.updatePosition();
  }

  addTo(layer) {
    layer.add(this.object);
  }

  updatePosition() {
    this.object.rotation.x = this.attitude.roll;
    this.object.rotation.y = this.attitude.yaw
    this.object.rotation.z = this.attitude.pitch;
    this.object.position.x = this.attitude.surge;
    this.object.position.y = this.attitude.heave + this.options.yOffset || 0;
    this.object.position.z = this.attitude.sway;
    this.object.updateMatrix();
  }

  getJoints() {
    const matrix = this.object.matrix;
    return this.jointPoints.map(v3 => v3.clone().applyMatrix4(matrix));
  }
}
