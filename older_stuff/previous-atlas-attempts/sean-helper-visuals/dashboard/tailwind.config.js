/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: '#0a0a0a',
        card: '#141414',
        border: '#222',
        'border-hover': '#333',
      },
    },
  },
  plugins: [],
}
