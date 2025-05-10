import type { Config } from 'tailwindcss';
import typography from '@tailwindcss/typography';

const config: Config = {
  // tell Tailwind which files to scan for class names
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        'finbot-bg': '#0a0a0a',
        'finbot-fg': '#ededed',
        'finbot-reply': '#1e293b', // slate-800
      },
    },
  },
  plugins: [typography],
};

export default config;