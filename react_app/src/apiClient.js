import axios from 'axios';

// Create the backend client
const hostIP = process.env.REACT_APP_HOST || '127.0.0.1';
const apiClient = axios.create({
  baseURL: `http://${hostIP}:5000`,
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
