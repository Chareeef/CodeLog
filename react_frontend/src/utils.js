import apiClient from './apiClient';

export function formatTime(milliseconds) {
  const seconds = Math.floor(milliseconds / 1000);
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  const formattedHours = hours > 0 ? String(hours).padStart(2, '0') + 'h:' : '';
  const formattedMinutes =
    minutes > 0 ? String(minutes).padStart(2, '0') + 'm:' : '';
  const formattedSeconds = String(secs).padStart(2, '0') + 's';

  return `${formattedHours}${formattedMinutes}${formattedSeconds}`;
}

export async function checkAuth(navigate) {
  try {
    await apiClient.get('/');
  } catch (error) {
    localStorage.removeItem('jwt_access_token');
    localStorage.removeItem('jwt_refresh_token');
    const alertMessage =
      'Sorry, it seems your Authentication was lost or corrupted. Please log in again.';
    navigate('/login', { state: { alertMessage: alertMessage } });
  }
}
