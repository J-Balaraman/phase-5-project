module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        bg: 'var(--bg)',
        header: 'var(--header)',
        link: 'var(--link)',
        text: 'var(--text)',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
