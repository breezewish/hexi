import request from 'axios';
import { Message } from 'element-ui';

const API = {
  input: {
    plugins() {
      return request.get('/core/input/api/plugins');
    },
    setEnabledPlugins(idList) {
      return request.post('/core/input/api/plugins/enabled', { id: idList });
    },
  },
};

export default API;
