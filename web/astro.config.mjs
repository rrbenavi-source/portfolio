// TODO(Task 9): set real Pages URL — replace site/base after confirming GitHub repo name
// For a project page: site = "https://<user>.github.io", base = "/<repo>/"
// For a custom domain:  site = "https://yourdomain.com", base = "/"
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://example.com',   // TODO(Task 9): update to real GitHub Pages URL
  base: '/',                     // TODO(Task 9): update to "/<repo>/" if using project page
  output: 'static',
  i18n: {
    defaultLocale: 'es',
    locales: ['es', 'en'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
});
