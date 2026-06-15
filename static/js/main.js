/* PostFlow — interações globais (jQuery + Bootstrap) */
(function ($) {
  'use strict';

  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
  }

  $.ajaxSetup({
    headers: { 'X-CSRFToken': getCookie('csrftoken') },
    beforeSend: function () {
      $('#loading-spinner').removeClass('d-none');
    },
    complete: function () {
      $('#loading-spinner').addClass('d-none');
    },
    error: function (xhr) {
      const msg = xhr.responseJSON?.error || 'Ocorreu um erro. Tente novamente.';
      if (window.showToast) window.showToast(msg);
    },
  });

  window.showToast = function (message) {
    const $toast = $('#toast');
    if (!$toast.length) return;
    $toast.text(message).addClass('show');
    setTimeout(function () {
      $toast.removeClass('show');
    }, 3000);
  };

  /* Modal de confirmação */
  const $modal = $('#confirm-modal');
  let $pendingForm = null;

  window.showConfirmModal = function (message, onConfirm) {
    if (!$modal.length) {
      if (window.confirm(message)) onConfirm();
      return;
    }
    $('#confirm-modal-message').text(message || 'Tem certeza que deseja continuar?');
    $modal.addClass('open');
    $('#confirm-modal-action').off('click').on('click', function () {
      $modal.removeClass('open');
      onConfirm();
    });
  };

  $('[data-dismiss-modal]').on('click', function () {
    $modal.removeClass('open');
    $pendingForm = null;
  });

  $(document).on('submit', '.js-confirm-delete', function (e) {
    e.preventDefault();
    const form = this;
    const message = $(form).data('message') || 'Confirmar esta ação?';
    showConfirmModal(message, function () {
      form.submit();
    });
  });

  /* Sidebar mobile */
  const $sidebar = $('.sidebar');
  const $backdrop = $('.sidebar-backdrop');

  $('.sidebar-toggle').on('click', function () {
    $sidebar.toggleClass('open');
    $backdrop.toggleClass('visible');
  });

  $backdrop.on('click', function () {
    $sidebar.removeClass('open');
    $backdrop.removeClass('visible');
  });

  /* Estilização de inputs de formulário Django */
  $('input:not([type=checkbox]):not([type=radio]):not([type=hidden]), select, textarea')
    .not('.input')
    .addClass('input form-control')
    .css('background', 'var(--bg-elevated)');

})(jQuery);
