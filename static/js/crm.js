/* ============================================================
   Selentra CRM – Base JavaScript
   ============================================================ */

(function () {
  'use strict';

  // Sidebar toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function () {
      const isMobile = window.innerWidth <= 768;
      if (isMobile) {
        sidebar.classList.toggle('mobile-open');
      } else {
        sidebar.classList.toggle('collapsed');
        try {
          localStorage.setItem('crm-sidebar-collapsed', sidebar.classList.contains('collapsed'));
        } catch (e) {}
      }
    });

    // Restore sidebar state on desktop
    try {
      if (window.innerWidth > 768 && localStorage.getItem('crm-sidebar-collapsed') === 'true') {
        sidebar.classList.add('collapsed');
      }
    } catch (e) {}
  }

  // Auto-dismiss alerts after 5 seconds
  document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // Confirm delete with data-confirm attribute
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!confirm(el.dataset.confirm || 'Are you sure?')) {
        e.preventDefault();
      }
    });
  });
})();
