/* Anderson Glass & Glazing */
(function () {
  'use strict';

  /* ---- theme ---- */
  var root = document.documentElement;
  try {
    var saved = localStorage.getItem('ag-theme');
    if (saved) root.setAttribute('data-theme', saved);
  } catch (e) {}

  function toggleTheme() {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('ag-theme', next); } catch (e) {}
    var btn = document.querySelector('[data-theme-toggle]');
    if (btn) btn.setAttribute('aria-label', next === 'light' ? 'Switch to dark theme' : 'Switch to light theme');
  }

  /* ---- header state ---- */
  var header = document.querySelector('.site-header');
  function onScroll() {
    if (!header) return;
    header.classList.toggle('is-stuck', window.scrollY > 24);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- drawer ---- */
  var drawer = document.querySelector('.drawer');
  var menuBtn = document.querySelector('[data-menu]');
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove('is-open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
  if (menuBtn && drawer) {
    menuBtn.addEventListener('click', function () {
      var open = drawer.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });
    drawer.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', closeDrawer); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDrawer(); });
  }

  /* ---- reveal ---- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---- gallery filter ---- */
  var chips = document.querySelectorAll('[data-filter]');
  var tiles = document.querySelectorAll('[data-tags]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.remove('is-active'); });
      chip.classList.add('is-active');
      var f = chip.getAttribute('data-filter');
      tiles.forEach(function (t) {
        var match = f === 'all' || (t.getAttribute('data-tags') || '').indexOf(f) > -1;
        t.style.display = match ? '' : 'none';
      });
    });
  });

  /* ---- lightbox ---- */
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('figcaption');
    document.querySelectorAll('[data-lightbox]').forEach(function (tile) {
      tile.addEventListener('click', function () {
        var img = tile.querySelector('img');
        lbImg.src = tile.getAttribute('data-full') || img.src;
        lbImg.alt = img.alt;
        lbCap.textContent = img.alt;
        lb.classList.add('is-open');
        document.body.style.overflow = 'hidden';
      });
    });
    function closeLb() { lb.classList.remove('is-open'); document.body.style.overflow = ''; }
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.closest('.lightbox-close')) closeLb(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLb(); });
  }

  /* ---- enquiry form -> mail composer ---- */
  var form = document.querySelector('[data-enquiry]');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var name = form.elements['name'].value.trim();
      var phone = form.elements['phone'].value.trim();
      var email = form.elements['email'].value.trim();
      var suburb = form.elements['suburb'].value.trim();
      var service = form.elements['service'].value;
      var message = form.elements['message'].value.trim();

      if (!name || !phone) {
        status.textContent = 'Please add your name and a phone number.';
        return;
      }

      var subject = 'Quote request — ' + service + (suburb ? ' — ' + suburb : '');
      var body = [
        'Name: ' + name,
        'Phone: ' + phone,
        email ? 'Email: ' + email : '',
        suburb ? 'Suburb: ' + suburb : '',
        'Service: ' + service,
        '',
        message,
        '',
        '— sent from andersonglass.com.au'
      ].filter(Boolean).join('\n');

      status.textContent = 'Opening your email app with the details filled in…';
      window.location.href = 'mailto:ben@andersonglass.com.au?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      setTimeout(function () {
        // static text only — no user input is interpolated here
        status.textContent = 'Nothing happened? Call 0414 441 192 or email ben@andersonglass.com.au.';
        var tel = document.createElement('a');
        tel.href = 'tel:+61414441192';
        tel.textContent = ' Tap to call.';
        tel.style.color = 'inherit';
        tel.style.textDecoration = 'underline';
        status.appendChild(tel);
      }, 1800);
    });
  }

  /* ---- count up ---- */
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && counters.length) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var target = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var start = performance.now();
        var dur = 1400;
        function step(t) {
          var p = Math.min((t - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = (target % 1 === 0 ? Math.round(target * eased) : (target * eased).toFixed(1)) + suffix;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
        co.unobserve(el);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  }

  /* ---- year ---- */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---- theme button ---- */
  document.querySelectorAll('[data-theme-toggle]').forEach(function (b) { b.addEventListener('click', toggleTheme); });

  /* ---- favourite: smooth anchor offset ---- */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.length < 2) return;
      var el = document.querySelector(id);
      if (!el) return;
      e.preventDefault();
      var y = el.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top: y, behavior: 'smooth' });
    });
  });
})();
