'use strict';

const projectToggles = document.querySelectorAll('.project-toggle');

projectToggles.forEach((toggle) => {
  toggle.addEventListener('click', () => {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true';
    const details = toggle.nextElementSibling;

    if (!details || !details.classList.contains('project-details')) {
      return;
    }

    toggle.setAttribute('aria-expanded', String(!isOpen));
    details.hidden = isOpen;
  });
});

const cvDownloadLink = document.querySelector('.download-button');

document.querySelectorAll('[data-print]').forEach((button) => {
  button.addEventListener('click', () => {
    if (!cvDownloadLink) {
      return;
    }

    const printWindow = window.open('', '_blank');

    if (!printWindow) {
      window.location.assign(cvDownloadLink.href);
      return;
    }

    printWindow.addEventListener('load', () => {
      window.setTimeout(() => {
        printWindow.focus();
        printWindow.print();
      }, 500);
    }, { once: true });

    printWindow.location.href = cvDownloadLink.href;
  });
});
