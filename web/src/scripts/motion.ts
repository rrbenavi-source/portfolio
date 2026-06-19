// Progressive-enhancement motion: scroll reveals + metric count-up.
// No-ops gracefully and respects prefers-reduced-motion.

const REVEAL_THRESHOLD = 0.12;
const COUNT_THRESHOLD = 0.5;
const COUNT_DURATION = 1100;

const TILT_MAX_DEG = 5;
const MAGNET_STRENGTH = 0.25;

function initTilt(): void {
  const cards = document.querySelectorAll<HTMLElement>('.card');
  cards.forEach((card) => {
    card.addEventListener('pointermove', (e) => {
      const rect = card.getBoundingClientRect();
      const px = (e.clientX - rect.left) / rect.width - 0.5;
      const py = (e.clientY - rect.top) / rect.height - 0.5;
      card.style.transform = `perspective(900px) rotateX(${(-py * TILT_MAX_DEG).toFixed(2)}deg) rotateY(${(px * TILT_MAX_DEG).toFixed(2)}deg) translateY(-4px)`;
    });
    card.addEventListener('pointerleave', () => {
      card.style.transform = '';
    });
  });
}

function initMagnetic(): void {
  const magnets = document.querySelectorAll<HTMLElement>('.btn-primary');
  magnets.forEach((el) => {
    el.addEventListener('pointermove', (e) => {
      const rect = el.getBoundingClientRect();
      const mx = e.clientX - rect.left - rect.width / 2;
      const my = e.clientY - rect.top - rect.height / 2;
      el.style.transform = `translate(${(mx * MAGNET_STRENGTH).toFixed(1)}px, ${(my * MAGNET_STRENGTH).toFixed(1)}px)`;
    });
    el.addEventListener('pointerleave', () => {
      el.style.transform = '';
    });
  });
}

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

  // Premium pointer interactions — fine pointers only, never under reduced-motion
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (!reduce && finePointer) {
    initTilt();
    initMagnetic();
  }
}
