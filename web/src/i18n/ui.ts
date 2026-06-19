import { dict as es } from './es';
import { dict as en } from './en';

export type Lang = 'es' | 'en';
export type Dict = typeof es;

export function getLangFromUrl(url: URL): Lang {
  return url.pathname.startsWith('/en') ? 'en' : 'es';
}

export function useTranslations(lang: Lang): Dict {
  return lang === 'en' ? en : es;
}

/**
 * Maps a path to its counterpart in the given target language.
 * ES root "/" <-> EN root "/en/"
 * ES "/casos/" <-> EN "/en/casos/"
 */
export function getAlternatePath(path: string, targetLang: Lang): string {
  if (targetLang === 'en') {
    // ES -> EN: prepend /en
    if (path === '/') return '/en/';
    return '/en' + path;
  } else {
    // EN -> ES: strip /en prefix
    if (path === '/en/' || path === '/en') return '/';
    return path.replace(/^\/en/, '');
  }
}
