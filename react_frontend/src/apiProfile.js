import axios from 'axios';

// Create the backend client
const hostIP = process.env.REACT_APP_HOST || 'http://code-log.site';
const apiProfile = axios.create({
  baseURL: `${hostIP}:5000/profile`, 
});

apiProfile.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('jwt_access_token');

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default apiProfile;
