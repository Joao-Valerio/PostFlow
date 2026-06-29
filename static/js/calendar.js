/* PostFlow — FullCalendar v6 + jQuery AJAX */
(function ($) {
  'use strict';

  const calendarEl = document.getElementById('calendar');
  if (!calendarEl || typeof FullCalendar === 'undefined') return;

  const eventsUrl = window.POSTFLOW_CALENDAR_EVENTS_URL;
  const rescheduleBase = window.POSTFLOW_CALENDAR_RESCHEDULE_URL || '';

  const platformColors = {
    facebook: '#1877F2',
    instagram: '#E4405F',
    linkedin: '#0A66C2',
    twitter: '#1DA1F2',
  };

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'pt-br',
    height: 'auto',
    expandRows: true,
    nowIndicator: true,
    slotMinTime: '06:00:00',
    slotMaxTime: '23:00:00',
    allDaySlot: false,
    slotEventOverlap: false,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,listWeek',
    },
    buttonText: {
      today: 'Hoje',
      month: 'Mês',
      week: 'Semana',
      list: 'Lista',
    },
    views: {
      dayGridMonth: {
        dayMaxEvents: 3,
      },
      timeGridWeek: {
        dayHeaderFormat: { weekday: 'short', day: 'numeric', omitCommas: true },
        slotLabelFormat: { hour: '2-digit', minute: '2-digit', hour12: false },
      },
      listWeek: {
        listDayFormat: { weekday: 'long', day: 'numeric', month: 'long' },
        listDaySideFormat: false,
      },
    },
    noEventsText: 'Nenhum agendamento neste período',
    editable: true,
    eventDrop: function (info) {
      const url = rescheduleBase + info.event.id + '/';
      $.ajax({
        url: url,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ start: info.event.start.toISOString() }),
      })
        .done(function () {
          if (window.showToast) {
            window.showToast('Agendamento reagendado com sucesso.');
          }
        })
        .fail(function () {
          info.revert();
          if (window.showToast) {
            window.showToast('Não foi possível reagendar. Tente novamente.');
          }
        });
    },
    events: function (info, successCallback, failureCallback) {
      $.getJSON(eventsUrl, {
        start: info.startStr,
        end: info.endStr,
      })
        .done(function (events) {
          const styled = events.map(function (ev) {
            const platform = ev.extendedProps?.platform;
            const color = platformColors[platform] || 'oklch(67% 0.09 160)';
            return Object.assign({}, ev, {
              backgroundColor: color,
              borderColor: 'transparent',
              textColor: '#ffffff',
            });
          });
          successCallback(styled);
        })
        .fail(function () {
          failureCallback();
          if (window.showToast) {
            window.showToast('Não foi possível carregar os eventos do calendário.');
          }
        });
    },
    eventDidMount: function (info) {
      info.el.style.borderRadius = '8px';
    },
    loading: function (isLoading) {
      $('#loading-spinner').toggleClass('d-none', !isLoading);
    },
  });

  calendar.render();
})(jQuery);
