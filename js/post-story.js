(function () {
  'use strict';
  var el = document.querySelector('[data-psh]');
  if (!el || typeof gsap === 'undefined') return;

  gsap.registerPlugin(ScrollTrigger);

  var p1 = el.querySelector('.psh-p1');
  var p2 = el.querySelector('.psh-p2');
  var p3 = el.querySelector('.psh-p3');
  var text = el.querySelector('.psh-text');

  var tl = gsap.timeline({
    scrollTrigger: {
      trigger: el,
      start: 'top top',
      end: 'bottom bottom',
      scrub: 1.4,
    }
  });

  tl
    // Ch1 → Ch2 crossfade (0.0 – 0.42)
    .to(p1,   { opacity: 0, scale: 1.06, duration: 0.40, ease: 'power2.inOut' }, 0.20)
    .to(p2,   { opacity: 1, scale: 1,    duration: 0.40, ease: 'power2.inOut' }, 0.26)
    // Ch2 → Ch3 crossfade (0.42 – 0.80)
    .to(p2,   { opacity: 0, scale: 1.06, duration: 0.40, ease: 'power2.inOut' }, 0.55)
    .to(p3,   { opacity: 1, scale: 1,    duration: 0.40, ease: 'power2.inOut' }, 0.61)
    // Title fade out near end
    .to(text, { opacity: 0, y: -28, duration: 0.28, ease: 'power2.in' }, 0.78);
})();
