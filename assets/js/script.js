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

document.querySelectorAll('[data-print]').forEach((button) => {
  button.addEventListener('click', () => window.print());
});
