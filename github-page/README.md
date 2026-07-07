# Ricardo Benavides — Portafolio / CV web

Página personal (one-page) de **Ricardo Benavides — Data Architect & BI Strategist**.
Sitio estático autocontenido en un solo archivo (`index.html`), sin dependencias ni build.

## Publicar en GitHub Pages

1. Crea un repositorio en GitHub. Para una URL limpia tipo `https://<usuario>.github.io`,
   nómbralo **`<tu-usuario>.github.io`**. (Cualquier otro nombre publica en
   `https://<usuario>.github.io/<repo>/`.)
2. Sube el contenido de esta carpeta (al menos `index.html`):
   ```bash
   cd "github-page"
   git init
   git add index.html README.md
   git commit -m "feat: portafolio CV web"
   git branch -M main
   git remote add origin https://github.com/<tu-usuario>/<repo>.git
   git push -u origin main
   ```
3. En GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   rama `main`, carpeta `/ (root)`. Guarda.
4. Espera ~1 min. Tu sitio quedará en la URL que indica esa misma sección.

## Personalización rápida

- **Colores:** edita las variables `--accent`, `--gold`, `--bg` en el bloque `:root` del `<style>`.
- **Contenido:** todo el texto está en el `<body>` (hero, métricas, experiencia, caso de éxito, contacto).
- **Métricas animadas:** atributos `data-count` y `data-suffix` en la sección de métricas del hero.
- **Foto:** opcionalmente agrega una imagen en el hero; recuerda `width`/`height` explícitos y `loading="eager"` + `fetchpriority="high"`.

## Notas técnicas

- Tipografías: Space Grotesk + Inter (Google Fonts, `font-display: swap`).
- Animaciones solo sobre `transform`/`opacity`; respeta `prefers-reduced-motion`.
- Responsive en 320 / 768 / 1024 / 1440. Sin scripts de terceros.
