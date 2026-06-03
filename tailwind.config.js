/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html'],
  theme: {
    extend: {
      colors: {
        primary: '#8B5CF6',
        'surface-dark': '#131313',
        'surface-container': '#1c1b1b',
        'surface-bright': '#3a3939',
        'input-bg': '#1e1e1e',
        'brand-purple': '#7c3aed',
        'brand-dark': '#0a0a0a',
        'card-dark': '#141414',
        'card-border': '#262626',
        'text-muted': '#9ca3af',
        'accent-purple': '#a78bfa',
        brand: {
          background: '#09090b',
          sidebar: '#111114',
          card: '#18181b',
          accent: '#8b5cf6',
          textMuted: '#a1a1aa',
          border: '#27272a',
        },
        aureon: {
          dark: '#0A0A0A',
          card: '#121212',
          purple: '#A78BFA',
          border: '#2D2D2D',
        },
        bank: {
          background: '#0a0a0a',
          sidebar: '#0c0c0c',
          border: '#1f1f1f',
          accent: '#a78bfa',
          accentHover: '#8b5cf6',
          muted: '#71717a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        custom: '4px',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
};
