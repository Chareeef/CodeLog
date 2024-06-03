import axios from 'axios';

// Create the backend client
let host = process.env.REACT_APP_HOST || 'http://127.0.0.1:5000';
if (process.env.REACT_APP_ENV === 'DEV' && process.env.REACT_APP_IP) {
  host = `http://${process.env.REACT_APP_IP}:5000`;
}

const apiClient = axios.create({
  baseURL: `${host}/api`,
});

apiClient.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('jwt_access_token');

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
