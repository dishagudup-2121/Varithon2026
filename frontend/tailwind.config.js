/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'saffron': {
          DEFAULT: '#F28C00',
          'deep': '#D96F00',
        },
        'earth': {
          DEFAULT: '#6B421F',
          'dark': '#3D2918',
        },
        'charcoal': '#171717',
        'ivory': '#FFFDF8',
        'cream': '#F8F1E5',
        'beige': '#EDE2D0',
      },
      fontFamily: {
        'sans': ['system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
        'heading': ['system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
