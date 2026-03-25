/* ═══════════════════════════════════════════════════════════════
   MFVD — Fábrica de Prompts
   Interactions, Animations & Scroll Effects
═══════════════════════════════════════════════════════════════ */

(() => {
  'use strict';

  /* ── Reveal on scroll (IntersectionObserver) ─────────────── */
  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('.reveal').forEach((el) => revealObserver.observe(el));

  /* ── Nav scroll state ─────────────────────────────────────── */
  const nav = document.getElementById('nav');
  let lastScrollY = 0;

  const onScroll = () => {
    const scrollY = window.scrollY;

    // Scrolled class for backdrop
    nav.classList.toggle('is-scrolled', scrollY > 60);

    // Hide/show nav on scroll direction
    if (scrollY > 200) {
      nav.style.transform = scrollY > lastScrollY ? 'translateY(-100%)' : 'translateY(0)';
    } else {
      nav.style.transform = 'translateY(0)';
    }

    lastScrollY = scrollY;
  };

  window.addEventListener('scroll', onScroll, { passive: true });

  /* ── Cursor glow ──────────────────────────────────────────── */
  const glow = document.createElement('div');
  glow.className = 'cursor-glow';
  document.body.appendChild(glow);

  let mouseX = 0, mouseY = 0;
  let glowX = 0, glowY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  const animateGlow = () => {
    glowX += (mouseX - glowX) * 0.08;
    glowY += (mouseY - glowY) * 0.08;
    glow.style.left = glowX + 'px';
    glow.style.top  = glowY + 'px';
    requestAnimationFrame(animateGlow);
  };
  animateGlow();

  // Hide glow when mouse leaves
  document.addEventListener('mouseleave', () => { glow.style.opacity = '0'; });
  document.addEventListener('mouseenter', () => { glow.style.opacity = '1'; });

  /* ── Parallax fruits on hero ──────────────────────────────── */
  const heroSection = document.getElementById('hero');
  const fruits = document.querySelectorAll('.hero .fruit');

  const depths = [0.06, 0.04, 0.08, 0.05, 0.07];

  window.addEventListener('mousemove', (e) => {
    if (!heroSection) return;
    const rect = heroSection.getBoundingClientRect();
    if (rect.bottom < 0) return;

    const cx = e.clientX - window.innerWidth / 2;
    const cy = e.clientY - window.innerHeight / 2;

    fruits.forEach((fruit, i) => {
      const depth = depths[i] ?? 0.05;
      const tx = cx * depth;
      const ty = cy * depth;
      fruit.style.transform += ` translate(${tx}px, ${ty}px)`;
    });
  }, { passive: true });

  /* ── Smooth scroll for anchor links ──────────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      if (!target) return;
      e.preventDefault();

      const offset = nav ? nav.offsetHeight + 24 : 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;

      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  /* ── Bottle tilt on mouse move ────────────────────────────── */
  const bottleWrap = document.querySelector('.hero__bottle');

  if (bottleWrap) {
    const bottleSection = bottleWrap.closest('.hero');

    bottleSection?.addEventListener('mousemove', (e) => {
      const rect = bottleSection.getBoundingClientRect();
      const relX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      const relY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;

      const rotX = relY * -8;
      const rotY = relX * 10;

      bottleWrap.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg)`;
    });

    bottleSection?.addEventListener('mouseleave', () => {
      bottleWrap.style.transform = 'rotateX(0) rotateY(0)';
    });
  }

  /* ── Counter animation for stats ─────────────────────────── */
  const statNumbers = document.querySelectorAll('.stat__number');

  const animateCount = (el) => {
    const raw = el.textContent.trim();
    const small = el.querySelector('small');
    const suffix = small ? small.textContent : '';
    const numStr = raw.replace(suffix, '').trim();
    const num = parseFloat(numStr);

    if (isNaN(num) || raw === '∞') return; // skip non-numeric

    const duration = 1400;
    const start = performance.now();
    const isFloat = numStr.includes('.');

    const update = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
      const current = eased * num;

      const display = isFloat ? current.toFixed(1) : Math.round(current);
      el.innerHTML = display + (suffix ? `<small>${suffix}</small>` : '');

      if (progress < 1) requestAnimationFrame(update);
    };

    requestAnimationFrame(update);
  };

  const statsObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          statsObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  statNumbers.forEach((el) => statsObserver.observe(el));

  /* ── Benefit cards stagger on reveal ─────────────────────── */
  const benefitCards = document.querySelectorAll('.benefit-card');
  benefitCards.forEach((card, i) => {
    card.style.transitionDelay = `${i * 0.1}s`;
  });

  /* ── Ingredient items stagger ─────────────────────────────── */
  document.querySelectorAll('.ingrediente-item').forEach((item, i) => {
    item.style.transitionDelay = `${i * 0.1}s`;
  });

  /* ── Scroll-driven bottle scale ──────────────────────────── */
  const bottle = document.querySelector('.bottle');
  if (bottle) {
    window.addEventListener('scroll', () => {
      const scrollRatio = Math.min(window.scrollY / (window.innerHeight * 0.6), 1);
      const scale = 1 - scrollRatio * 0.08;
      bottle.style.transform = `scale(${scale})`;
    }, { passive: true });
  }

  /* ── Reduced motion support ──────────────────────────────── */
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.fruit, .hero__bg-orb, .ingrediente-item__ring').forEach((el) => {
      el.style.animation = 'none';
    });
    document.querySelectorAll('.hero__bottle').forEach((el) => {
      el.style.animation = 'none';
    });
  }

  /* ── Init: trigger visible reveals above fold ─────────────── */
  window.dispatchEvent(new Event('scroll'));

})();
