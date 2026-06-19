import { dict as es } from './es';
import { dict as en } from './en';

export type Lang = 'es' | 'en';
export type Dict = typeof es;

export function getLangFromUrl(url: URL): Lang {
  return url.pathname.startsWith('/en') ? 'en' : 'es';
}

export function useTranslations(lang: Lang): Dict {
  return lang === 'en' ? (en as unknown as Dict) : es;
}

/**
 * Prefixes a root-absolute app path with the configured base
 * (e.g. "/portfolio/"), collapsing duplicate slashes. External URLs
 * (http/mailto) and already-prefixed paths pass through unchanged.
 */
export function withBase(path: string): string {
  if (/^(https?:|mailto:|#)/.test(path)) return path;
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  if (base && path.startsWith(base + '/')) return path;
  return (base + path).replace(/\/{2,}/g, '/');
}

/**
 * Maps a root-absolute path to its counterpart language and returns it
 * already base-prefixed. ES root "/" <-> EN root "/en/".
 */
export function getAlternatePath(path: string, targetLang: Lang): string {
  let mapped: string;
  if (targetLang === 'en') {
    mapped = path === '/' ? '/en/' : '/en' + path;
  } else {
    mapped = path === '/en/' || path === '/en' ? '/' : path.replace(/^\/en/, '');
  }
  return withBase(mapped);
}
