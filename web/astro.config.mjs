import { defineConfig } from 'astro/config';

// GitHub Pages project site: https://rrbenavi-source.github.io/portfolio/
export default defineConfig({
  site: 'https://rrbenavi-source.github.io',
  base: '/portfolio/',
  output: 'static',
  i18n: {
    defaultLocale: 'es',
    locales: ['es', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
});
