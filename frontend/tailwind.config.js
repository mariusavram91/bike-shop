// tailwind.config.js

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './public/**/*.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#42b983',
        secondary: '#111827',
      },
    },
  },
  plugins: [],
}
