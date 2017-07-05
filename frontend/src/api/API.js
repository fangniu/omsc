import axios from 'axios';
import config from './config';

class API {
  get (param) {
    config.url = param.url;
    config.method = 'GET';
    return axios(config);
  }
  post (param) {
    config.url = param.url;
    config.data = param.data;
    config.method = 'POST';
    return axios(config);
  }
  put (param) {
    config.url = param.url;
    config.data = param.data;
    config.method = 'PUT';
    return axios(config);
  }
  delete (param) {
    config.url = param.url;
    config.method = 'DELETE';
    return axios(config);
  }
  reqSuccess(obj,msg){
    obj.$message({
      message: msg,
      type: 'success'
    });
  }
  reqFail(obj,msg){
    obj.$message({
      message: msg,
      type: 'success'
    });
  }
}
export default API;
