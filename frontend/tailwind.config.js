/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],  // Roboto as the global/default font
        heading: ['Lexend', 'sans-serif'], // Lexend for special headers
      },
    },
  },
  plugins: [],
}
