export function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  const formattedHours =
    hours > 0 ? String(hours).padStart(2, '0') + 'h:' : '';
  const formattedMinutes =
    minutes > 0 ? String(minutes).padStart(2, '0') + 'm:' : '';
  const formattedSeconds = String(secs).padStart(2, '0') + 's';

  return `${formattedHours}${formattedMinutes}${formattedSeconds}`;
}
