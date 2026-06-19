// Progressive-enhancement motion: scroll reveals + metric count-up.
// No-ops gracefully and respects prefers-reduced-motion.

const REVEAL_THRESHOLD = 0.12;
const COUNT_THRESHOLD = 0.5;
const COUNT_DURATION = 1100;

export function initMotion(): void {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Reveal on scroll
  const reveals = document.querySelectorAll<HTMLElement>('.reveal');
  const revealIO = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          revealIO.unobserve(entry.target);
        }
      });
    },
    { threshold: REVEAL_THRESHOLD }
  );
  reveals.forEach((el) => revealIO.observe(el));

  // Count-up metrics
  const counters = document.querySelectorAll<HTMLElement>('[data-count]');
  const countIO = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target as HTMLElement;
        const target = parseInt(el.dataset.count ?? '0', 10);
        const suffix = el.dataset.suffix ?? '';

        if (reduce) {
          el.textContent = target + suffix;
          countIO.unobserve(el);
          return;
        }

        const start = performance.now();
        const tick = (now: number): void => {
          const p = Math.min((now - start) / COUNT_DURATION, 1);
          const eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
        countIO.unobserve(el);
      });
    },
    { threshold: COUNT_THRESHOLD }
  );
  counters.forEach((el) => countIO.observe(el));
}
