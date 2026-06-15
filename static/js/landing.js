/* PostFlow — interações da landing page */
(function () {
  'use strict';

  document.querySelectorAll('.faq-item').forEach(function (item) {
    var btn = item.querySelector('.faq-question');
    btn?.addEventListener('click', function () {
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (i) {
        i.classList.remove('open');
      });
      if (!isOpen) item.classList.add('open');
    });
  });

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('[data-animate]').forEach(function (el) {
    observer.observe(el);
  });
})();
