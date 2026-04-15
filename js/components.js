/* Shared header, footer, and utilities for the CCC Google microsite */

function renderHeader(activePage) {
  const pages = [
    { id: 'home', label: 'Overview', href: 'index.html' },
    { id: 'courses', label: 'Courses', href: 'courses.html' },
    { id: 'cpl', label: 'CPL Pathways', href: 'cpl.html' },
    { id: 'faq', label: 'FAQ', href: 'faq.html' },
    { id: 'getting-started', label: 'Get Started', href: 'getting-started.html' },
    { id: 'entrepreneurship', label: 'Innovation', href: 'entrepreneurship.html' },
    { id: 'pd', label: 'Prof. Development', href: 'professional-development.html' },
  ];

  const navLinks = pages.map(p =>
    `<a href="${p.href}" class="${p.id === activePage ? 'active' : ''}">${p.label}</a>`
  ).join('');

  return `
  <div class="gradient-bar"></div>
  <header class="site-header">
    <a href="index.html" class="brand">
      <img src="https://ai.cccco.edu/wp-content/uploads/2026/02/cccco-seal-rev-2.svg" alt="CCCCO" width="40" height="40">
      <span class="brand-text">CCCCO AI</span>
    </a>
    <button class="mobile-toggle" onclick="this.nextElementSibling.classList.toggle('open')" aria-label="Menu">&#9776;</button>
    <nav>${navLinks}</nav>
  </header>`;
}

function renderFooter() {
  return `
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-col">
        <h3>California Community Colleges<br>Chancellor's Office</h3>
        <p>1102 Q Street, 6th Floor<br>Sacramento, CA 95811<br>916-445-8752<br><a href="mailto:info@cccco.edu">info@cccco.edu</a></p>
        <div class="social-links" style="margin-top:1rem;">
          <a href="https://www.linkedin.com/company/californiacommunitycolleges" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M19.7,3H4.3C3.582,3,3,3.582,3,4.3v15.4C3,20.418,3.582,21,4.3,21h15.4c0.718,0,1.3-0.582,1.3-1.3V4.3C21,3.582,20.418,3,19.7,3z M8.339,18.338H5.667v-8.59h2.672V18.338z M7.004,8.574c-0.857,0-1.549-0.694-1.549-1.548c0-0.855,0.691-1.548,1.549-1.548c0.854,0,1.547,0.694,1.547,1.548C8.551,7.881,7.858,8.574,7.004,8.574z M18.339,18.338h-2.669v-4.177c0-0.996-0.017-2.278-1.387-2.278c-1.389,0-1.601,1.086-1.601,2.206v4.249h-2.667v-8.59h2.559v1.174h0.037c0.356-0.675,1.227-1.387,2.526-1.387c2.703,0,3.203,1.779,3.203,4.092V18.338z"/></svg></a>
          <a href="https://www.instagram.com/californiacommunitycolleges/" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12,4.622c2.403,0,2.688,0.009,3.637,0.052c0.877,0.04,1.354,0.187,1.671,0.31c0.42,0.163,0.72,0.358,1.035,0.673c0.315,0.315,0.51,0.615,0.673,1.035c0.123,0.317,0.27,0.794,0.31,1.671c0.043,0.949,0.052,1.234,0.052,3.637s-0.009,2.688-0.052,3.637c-0.04,0.877-0.187,1.354-0.31,1.671c-0.163,0.42-0.358,0.72-0.673,1.035c-0.315,0.315-0.615,0.51-1.035,0.673c-0.317,0.123-0.794,0.27-1.671,0.31c-0.949,0.043-1.233,0.052-3.637,0.052s-2.688-0.009-3.637-0.052c-0.877-0.04-1.354-0.187-1.671-0.31c-0.42-0.163-0.72-0.358-1.035-0.673c-0.315-0.315-0.51-0.615-0.673-1.035c-0.123-0.317-0.27-0.794-0.31-1.671C4.631,14.688,4.622,14.403,4.622,12s0.009-2.688,0.052-3.637c0.04-0.877,0.187-1.354,0.31-1.671c0.163-0.42,0.358-0.72,0.673-1.035c0.315-0.315,0.615-0.51,1.035-0.673c0.317-0.123,0.794-0.27,1.671-0.31C9.312,4.631,9.597,4.622,12,4.622 M12,3C9.556,3,9.249,3.01,8.289,3.054C7.331,3.098,6.677,3.25,6.105,3.472C5.513,3.702,5.011,4.01,4.511,4.511c-0.5,0.5-0.808,1.002-1.038,1.594C3.25,6.677,3.098,7.331,3.054,8.289C3.01,9.249,3,9.556,3,12c0,2.444,0.01,2.751,0.054,3.711c0.044,0.958,0.196,1.612,0.418,2.185c0.23,0.592,0.538,1.094,1.038,1.594c0.5,0.5,1.002,0.808,1.594,1.038c0.572,0.222,1.227,0.375,2.185,0.418C9.249,20.99,9.556,21,12,21s2.751-0.01,3.711-0.054c0.958-0.044,1.612-0.196,2.185-0.418c0.592-0.23,1.094-0.538,1.594-1.038c0.5-0.5,0.808-1.002,1.038-1.594c0.222-0.572,0.375-1.227,0.418-2.185C20.99,14.751,21,14.444,21,12s-0.01-2.751-0.054-3.711c-0.044-0.958-0.196-1.612-0.418-2.185c-0.23-0.592-0.538-1.094-1.038-1.594c-0.5-0.5-1.002-0.808-1.594-1.038c-0.572-0.222-1.227-0.375-2.185-0.418C14.751,3.01,14.444,3,12,3L12,3z M12,7.378c-2.552,0-4.622,2.069-4.622,4.622S9.448,16.622,12,16.622s4.622-2.069,4.622-4.622S14.552,7.378,12,7.378z M12,15c-1.657,0-3-1.343-3-3s1.343-3,3-3s3,1.343,3,3S13.657,15,12,15z M16.804,6.116c-0.596,0-1.08,0.484-1.08,1.08s0.484,1.08,1.08,1.08c0.596,0,1.08-0.484,1.08-1.08S17.401,6.116,16.804,6.116z"/></svg></a>
          <a href="https://www.youtube.com/user/CACommunityColleges" aria-label="YouTube"><svg viewBox="0 0 24 24"><path d="M21.8,8.001c0,0-0.195-1.378-0.795-1.985c-0.76-0.797-1.613-0.801-2.004-0.847c-2.799-0.202-6.997-0.202-6.997-0.202h-0.009c0,0-4.198,0-6.997,0.202C4.608,5.216,3.756,5.22,2.995,6.016C2.395,6.623,2.2,8.001,2.2,8.001S2,9.62,2,11.238v1.517c0,1.618,0.2,3.237,0.2,3.237s0.195,1.378,0.795,1.985c0.761,0.797,1.76,0.771,2.205,0.855c1.6,0.153,6.8,0.201,6.8,0.201s4.203-0.006,7.001-0.209c0.391-0.047,1.243-0.051,2.004-0.847c0.6-0.607,0.795-1.985,0.795-1.985s0.2-1.618,0.2-3.237v-1.517C22,9.62,21.8,8.001,21.8,8.001z M9.935,14.594l-0.001-5.62l5.404,2.82L9.935,14.594z"/></svg></a>
        </div>
      </div>
      <div class="footer-col">
        <h3>About This Initiative</h3>
        <p>The Google Tools and Certifications Rollout is a systemwide effort by the California Community Colleges Chancellor's Office, developed in partnership with San Jose City College, to bring Google's AI tools and career certificates to all 116 community colleges at no cost.</p>
      </div>
      <div class="footer-col">
        <h3>Quick Links</h3>
        <p>
          <a href="https://ai.cccco.edu/">CCCCO AI Microsite</a><br>
          <a href="https://ai.cccco.edu/initiatives/">Featured Initiatives</a><br>
          <a href="https://www.cccco.edu/">CCCCO.edu</a><br>
          <a href="https://lor.instructure.com/">Canvas Commons</a><br>
          <a href="https://cccdigitalcenter.org/projects/google-1.html">Digital Center — Google</a>
        </p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Google and Coursera are trademarks of their respective owners.</p>
      <div class="cc-badge">CC BY 4.0 — Free to use, adapt, and share with attribution</div>
    </div>
  </footer>`;
}

/* FAQ accordion */
function initFaqAccordion() {
  document.querySelectorAll('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const wasOpen = item.classList.contains('open');
      // Close all in same group
      item.closest('.faq-group')?.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });
}

/* Course filter */
function filterCourses(filter, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.course-card').forEach(card => {
    const tier = card.dataset.tier;
    const isCpl = card.dataset.cpl === 'yes';
    let show = false;
    if (filter === 'all') show = true;
    else if (filter === 'tier1') show = (tier === 'tier1');
    else if (filter === 'tier2') show = (tier === 'tier2');
    else if (filter === 'cpl') show = isCpl;
    card.style.display = show ? '' : 'none';
  });
  document.querySelectorAll('.tier-divider').forEach(div => {
    const tier = div.dataset.tier;
    if (filter === 'all' || filter === 'cpl') div.style.display = '';
    else div.style.display = (tier === filter) ? '' : 'none';
  });
}

/* Init: insert header + footer */
document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.page || 'home';
  const headerEl = document.getElementById('site-header');
  const footerEl = document.getElementById('site-footer');
  if (headerEl) headerEl.innerHTML = renderHeader(page);
  if (footerEl) footerEl.innerHTML = renderFooter();
  initFaqAccordion();
});
