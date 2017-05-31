import request from 'axios';
import { Notification } from 'element-ui';

request.interceptors.response.use(resp => {
  if (resp.status === 200) {
    const serverData = resp.data;
    resp.status = serverData.code;
    resp.data = serverData.data;
    if (resp.status !== 200) {
      const err = new Error(`错误: ${serverData.reason}`);
      err.response = resp;
      throw err;
    }
  }
  return resp;
});

request.interceptors.response.use(null, err => {
  Notification.error({
    title: '请求失败',
    message: err.message,
  });
  return Promise.reject(err);
});

const API = {
  enabledPlugins: {
    get(type) {
      return request.get(`/core/${type}/api/plugins`);
    },
    set(type, idList) {
      return request.post(`/core/${type}/api/plugins/enabled`, { id: idList });
    },
  },
};

export default API;
