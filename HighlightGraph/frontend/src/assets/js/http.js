import axios from 'axios'

axios.defaults.baseURL = 'http://192.168.3.70:8000';
axios.defaults.withCredentials = true;
axios.defaults.headers.post['Content-Type'] = 'application/json' //'application/x-www-form-urlencoded';

export default axios;