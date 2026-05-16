/* grove.js — Grovemade-exact nav scroll behavior */
(function () {
  var navbar = document.getElementById('navbar');
  if (!navbar) return;

  function onScroll() {
    if (window.scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* GO UP button */
  var goUp = document.getElementById('go-up');
  if (goUp) {
    goUp.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* Newsletter form */
  var forms = document.querySelectorAll('.v2-footer__email-form');
  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = form.querySelector('.v2-footer__email-input');
      var btn = form.querySelector('.v2-footer__email-submit');
      if (input && input.value) {
        btn.textContent = 'Subscribed';
        input.value = '';
        input.disabled = true;
        btn.disabled = true;
      }
    });
  });
})();
