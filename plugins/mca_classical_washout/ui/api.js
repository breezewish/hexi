import request from 'axios';

const API = {
  config: {
    scale: {
      get() {
        return request.get('/plugins/mca_classical_washout/api/config/scale');
      },
      set(config) {
        return request.post('/plugins/mca_classical_washout/api/config/scale', config);
      },
    },
  },
};

export default API;
