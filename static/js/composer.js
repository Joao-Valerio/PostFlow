(function () {
  'use strict';

  const limits = window.POSTFLOW_PLATFORM_LIMITS || {};
  const contentField = document.getElementById('id_content');
  const titleField = document.getElementById('id_title');
  if (!contentField) return;

  const previewTitle = document.querySelector('[data-preview-title]');
  const previewContent = document.querySelector('[data-preview-content]');
  const currentCount = document.querySelector('[data-current-count]');
  const platformInputs = Array.from(document.querySelectorAll('[data-platform-option]'));
  const platformBadges = Array.from(document.querySelectorAll('[data-limit]'));

  function updatePreview() {
    const content = (contentField.value || '').trim();
    const title = titleField ? (titleField.value || '').trim() : '';
    const count = content.length;

    if (previewTitle) previewTitle.textContent = title || 'Sem título';
    if (previewContent) {
      previewContent.textContent = content || 'O conteúdo aparece aqui conforme você digita.';
    }
    if (currentCount) currentCount.textContent = count;

    platformBadges.forEach((badge) => {
      const key = badge.getAttribute('data-limit');
      const limit = limits[key] || 0;
      badge.textContent = `${count}/${limit}`;
      badge.classList.toggle('text-danger', limit > 0 && count > limit);
    });
  }

  function updatePlatformStates() {
    platformInputs.forEach((input) => {
      const chip = input.closest('[data-platform-chip]');
      if (!chip) return;
      chip.setAttribute('data-active', input.checked ? 'true' : 'false');
    });
  }

  contentField.addEventListener('input', updatePreview);
  if (titleField) {
    titleField.addEventListener('input', updatePreview);
  }
  platformInputs.forEach((input) => input.addEventListener('change', updatePlatformStates));

  updatePreview();
  updatePlatformStates();
})();
