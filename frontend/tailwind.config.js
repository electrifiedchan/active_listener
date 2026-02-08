/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          black: '#0a0a0a',
          dark: '#121212',
          gray: '#1e1e1e',
          primary: '#00f0ff', // Cyberpunk Cyan
          secondary: '#ff003c', // Cyberpunk Red
          accent: '#fcee0a', // Cyberpunk Yellow
        },
      },
      fontFamily: {
        mono: ['"Courier New"', 'monospace'], // Hacker Font
      },
    },
  },
  plugins: [],
}