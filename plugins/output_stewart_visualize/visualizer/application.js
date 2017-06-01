import * as THREE from 'three';
import dat from 'dat.gui/build/dat.gui.js';
import Stats from 'stats.js';
import OrbitControlsFactory from 'three-orbit-controls';
import StewartPlatform from '@/platform/stewart';
import WebSocket from 'reconnecting-websocket';

const OrbitControls = OrbitControlsFactory(THREE);

class Application {
  constructor() {
    this._updateAttitude = this.updateAttitude.bind(this);
    this._animate = this.animate.bind(this);

    this.camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 1, 10000);
    this.camera.position.set(200, 180, 400);

    this.scene = new THREE.Scene();
    this.scene.add(this.camera);

    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setClearColor(0xf0f0f0);
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.shadowMap.enabled = true;
    document.body.appendChild(this.renderer.domElement);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.damping = 0.2;
    this.controls.target.set(0, 50, 0);

    window.addEventListener('resize', this.onWindowResize.bind(this), false);

    this.initDataChannel();
    this.initStats();
    this.initScene();
    this.initControl();

    this._animate();
  }

  initStats() {
    this.stats = new Stats();
    this.stats.showPanel(0);
    document.body.appendChild(this.stats.dom);
  }

  initScene() {
    this.scene.fog = new THREE.Fog(0xf0f0f0, 0.015, 2000);
    this.scene.add(new THREE.AmbientLight(0xf0f0f0));

    const light = new THREE.SpotLight(0xffffff, 1.5);
    light.position.set(-1000, 1500, 100);
    light.castShadow = true;
    light.shadow = new THREE.LightShadow(new THREE.PerspectiveCamera(70, 1, 200, 2000));
    light.shadow.bias = -0.000222;
    light.shadow.mapSize.width = 1024;
    light.shadow.mapSize.height = 1024;
    this.scene.add(light);

    const helper = new THREE.GridHelper(5000, 100);
    helper.position.y = 0;
    helper.material.opacity = 0.25;
    helper.material.transparent = true;
    this.scene.add(helper);

    const planeGeometry = new THREE.PlaneGeometry(5000, 5000);
    planeGeometry.rotateX(-Math.PI / 2);
    const planeMaterial = new THREE.ShadowMaterial({ opacity: 0.2 });
    const plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.position.y = -1;
    plane.receiveShadow = true;
    this.scene.add(plane);

    const axis = new THREE.AxisHelper(200);
    axis.position.set(0, 0, 0);
    this.scene.add(axis);

    this.stewart = new StewartPlatform();
    this.stewart.addTo(this.scene);
  }

  initDataChannel() {
    const ws = new WebSocket(`ws://${location.host}/plugins/output_stewart_visualize/api/signal`);
    ws.addEventListener('open', () => {
      console.log('WS Connection Established');
    });
    ws.addEventListener('message', ev => {
      console.log(ev.data);
    });
  }

  initControl() {
    this.controlOptions = {
      effects: {
        animate: true,
      },
      attitude: {
        pitch: 0, // rotateZ
        roll: 0,  // rotateX
        yaw: 0,   // rotateY
        surge: 0, // x
        sway: 0,  // z
        heave: 0, // y
      },
    },
    this.gui = new dat.GUI();
    const fEffects = this.gui.addFolder('Effects');
    fEffects.add(this.controlOptions.effects, 'animate');
    fEffects.open();
    const fAttitude = this.gui.addFolder('Platform Attitude');
    fAttitude.add(this.controlOptions.attitude, 'pitch', -45, 45).onChange(this._updateAttitude);
    fAttitude.add(this.controlOptions.attitude, 'roll', -45, 45).onChange(this._updateAttitude);
    fAttitude.add(this.controlOptions.attitude, 'yaw', -45, 45).onChange(this._updateAttitude);
    fAttitude.add(this.controlOptions.attitude, 'surge', -50, 50).onChange(this._updateAttitude);
    fAttitude.add(this.controlOptions.attitude, 'sway', -50, 50).onChange(this._updateAttitude);
    fAttitude.add(this.controlOptions.attitude, 'heave', -50, 50).onChange(this._updateAttitude);
    fAttitude.open();
  }

  updateAttitude() {
    this.stewart.setAttitude({
      pitch: THREE.Math.degToRad(this.controlOptions.attitude.pitch),
      roll: -THREE.Math.degToRad(this.controlOptions.attitude.roll),
      yaw: THREE.Math.degToRad(this.controlOptions.attitude.yaw),
      surge: -this.controlOptions.attitude.surge,
      sway: -this.controlOptions.attitude.sway,
      heave: this.controlOptions.attitude.heave,
    });
  }

  onWindowResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  animate(timestamp) {
    this.stats.begin();
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
    this.stats.end();
    requestAnimationFrame(this._animate);
  }
}

const app = new Application();
export default app;
