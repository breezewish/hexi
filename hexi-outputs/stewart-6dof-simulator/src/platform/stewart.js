import * as THREE from 'three';
import Plate from './plate';
import Leg from './leg';
import Chair from './chair';

export default class StewartPlatform {
  constructor() {
    this.group = new THREE.Group();

    this.base = new Plate({
      radius: 120,
      jointRadius: 110,
      innerRadius: 100,
      alphaDeg: 10,
      thickness: 10,
      yOffset: 0,
    });
    this.base.addTo(this.group);

    this.top = new Plate({
      radius: 70,
      jointRadius: 60,
      innerRadius: 0,
      alphaDeg: 10,
      thickness: 10,
      yOffset: 100,
      reverse: true,
    });
    this.top.addTo(this.group);

    const jointsTop = this.top.getJoints();
    const jointsBase = this.base.getJoints();

    this.legs = [];
    for (let i = 0; i < 6; ++i) {
      const leg = new Leg({
        p1: jointsBase[i],
        p2: jointsTop[(i + 3) % 6],
        radius: 5,
      });
      leg.addTo(this.group);
      this.legs.push(leg);
    }

    this.chair = new Chair({
      material: {
        color: 0x666666,
        roughness: 0.8,
        metalness: 0.5,
      },
      yOffset: 100,
    });
    this.chair.addTo(this.group);
  }

  addTo(layer) {
    layer.add(this.group);
  }

  setAttitude(attitude) {
    this.top.attitude = attitude;
    this.top.updatePosition();

    const jointsTop = this.top.getJoints();
    const jointsBase = this.base.getJoints();
    for (let i = 0; i < 6; ++i) {
      this.legs[i].updateEndpoints(jointsBase[i], jointsTop[(i + 3) % 6]);
    }

    this.chair.attitude = attitude;
    this.chair.updatePosition();
  }
}
