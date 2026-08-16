/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        'notion-bg': '#ffffff',
        'notion-sidebar': '#f7f6f3',
        'notion-border': '#e9e9e7',
        'notion-text': '#37352f',
        'notion-text-light': '#787774',
        'notion-blue': '#2383e2',
        'notion-hover': '#f1f1ef',
      },
    },
  },
  plugins: [],
}
