import request from 'axios';

const API = {
  state: {
    set(stateId) {
      return request.post('/plugins/input_flight_attitude/api/state', { state: stateId });
    },
  },
};

export default API;
