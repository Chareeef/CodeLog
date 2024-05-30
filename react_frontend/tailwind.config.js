
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'grey': '#333',
        'beige': '#F2E6CE',
        'brown': '#593C2C',
        'orange':  '#D96236',
        'green': '#103B40',
        'glight': '#1d6b74',
        'rose': '#ffded7',
        'olight': '#D98C5F',
      }
    },
  },
  plugins: [],
}