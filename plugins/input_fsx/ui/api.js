import request from 'axios';

const API = {
  config: {
    get() {
      return request.get('/plugins/input_fsx/api/config');
    },
    set(config) {
      return request.post('/plugins/input_fsx/api/config', config);
    },
  },
};

export default API;
