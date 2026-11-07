/* Anderson Glass & Glazing */
(function () {
  'use strict';
  var root = document.documentElement;

  /* theme: paper (default) <-> blueprint (dark) */
  try {
    var saved = localStorage.getItem('ag-scheme');
    if (saved) root.setAttribute('data-theme', saved);
  } catch (e) {}

  function toggleTheme() {
    var next = root.getAttribute('data-theme') === 'blueprint' ? 'paper' : 'blueprint';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('ag-scheme', next); } catch (e) {}
    var btn = document.querySelector('[data-theme-toggle]');
    if (btn) btn.setAttribute('aria-label', next === 'blueprint' ? 'Switch to paper theme' : 'Switch to blueprint theme');
  }
  document.querySelectorAll('[data-theme-toggle]').forEach(function (b) { b.addEventListener('click', toggleTheme); });

  /* sticky header shade */
  var head = document.querySelector('.tblock');
  function onScroll() { if (head) head.style.boxShadow = window.scrollY > 12 ? '0 10px 30px -24px rgba(0,0,0,.6)' : 'none'; }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* drawer */
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

  /* reveal */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add('is-in'); }); }

  /* gallery filters */
  var chips = document.querySelectorAll('[data-filter]');
  var plates = document.querySelectorAll('[data-tags]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.classList.remove('is-active'); });
      chip.classList.add('is-active');
      var f = chip.getAttribute('data-filter');
      plates.forEach(function (t) {
        t.style.display = (f === 'all' || (t.getAttribute('data-tags') || '').indexOf(f) > -1) ? '' : 'none';
      });
    });
  });

  /* lightbox */
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption');
    document.querySelectorAll('[data-lightbox]').forEach(function (pl) {
      pl.addEventListener('click', function () {
        var img = pl.querySelector('img');
        lbImg.src = pl.getAttribute('data-full') || img.src;
        lbImg.alt = img.alt; lbCap.textContent = img.alt;
        lb.classList.add('is-open'); document.body.style.overflow = 'hidden';
      });
    });
    function closeLb() { lb.classList.remove('is-open'); document.body.style.overflow = ''; }
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.closest('.lightbox-close')) closeLb(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLb(); });
  }

  /* enquiry -> API, with mail-composer fallback */
  var form = document.querySelector('[data-enquiry]');
  if (form) {
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var btn = form.querySelector('button[type=submit]');
      var v = function (n) { return (form.elements[n] && form.elements[n].value || '').trim(); };
      var name = v('name'), phone = v('phone'), email = v('email'), suburb = v('suburb'),
          service = v('service'), message = v('message'), trap = v('company_website');

      if (!name || !phone) { status.textContent = 'Add your name and a phone number.'; return; }

      var payload = {
        name: name, phone: phone, email: email, suburb: suburb,
        service: service, message: message, company_website: trap,
        page: location.pathname
      };

      // optional photos — limits mirror the worker so we fail fast and explain why.
      // Deliberately permissive: an iPhone photo is a photo whatever container it uses.
      var LIMITS = { files: 4, perFile: 8 * 1024 * 1024, total: 20 * 1024 * 1024 };
      var picker = form.querySelector('input[name=photos]');
      var files = picker && picker.files ? Array.prototype.slice.call(picker.files) : [];

      if (files.length > LIMITS.files) {
        status.textContent = 'Up to ' + LIMITS.files + ' photos, please.'; return;
      }

      // Normalise everything the browser can decode into a JPEG: HEIC from iPhones,
      // PNG, WebP, GIF, TIFF. If the browser cannot decode it (Chrome + HEIC), the
      // original is sent unchanged and the server accepts it.
      async function normalise(f) {
        if (!window.createImageBitmap) return f;
        try {
          var bmp = await createImageBitmap(f);
          var scale = Math.min(1, 2400 / Math.max(bmp.width, bmp.height));
          var w = Math.max(1, Math.round(bmp.width * scale));
          var h = Math.max(1, Math.round(bmp.height * scale));
          var c = document.createElement('canvas');
          c.width = w; c.height = h;
          c.getContext('2d').drawImage(bmp, 0, 0, w, h);
          var blob = await new Promise(function (res) { c.toBlob(res, 'image/jpeg', 0.85); });
          if (!blob) return f;
          return new File([blob], f.name.replace(/\.[^.]+$/, '') + '.jpg', { type: 'image/jpeg' });
        } catch (err) {
          return f;
        }
      }

      if (files.length) {
        status.textContent = 'Preparing photos…';
        var out = [];
        for (var j = 0; j < files.length; j++) {
          out.push(await normalise(files[j]));
        }
        files = out;
      }

      var totalBytes = 0;
      for (var i = 0; i < files.length; i++) {
        var f = files[i];
        if (f.size > LIMITS.perFile) {
          status.textContent = '"' + f.name + '" is too large — try a smaller photo.'; return;
        }
        totalBytes += f.size;
      }
      if (totalBytes > LIMITS.total) {
        status.textContent = 'Those photos are too big together — send fewer, or send two batches.'; return;
      }

      function mailto() {
        var subject = 'Quote request — ' + service + (suburb ? ' — ' + suburb : '');
        var body = [
          'Name: ' + name, 'Phone: ' + phone,
          email ? 'Email: ' + email : '', suburb ? 'Suburb: ' + suburb : '',
          'Service: ' + service, '', message, '', '— sent from andersonglass.com.au'
        ].filter(Boolean).join('\n');
        window.location.href = 'mailto:ben@andersonglass.com.au?subject=' +
          encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
        setTimeout(function () {
          status.textContent = 'Nothing happened? Call 0414 441 192 or email ben@andersonglass.com.au.';
          var tel = document.createElement('a');
          tel.href = 'tel:+61414441192'; tel.textContent = ' Tap to call.';
          tel.style.color = 'inherit'; tel.style.textDecoration = 'underline';
          status.appendChild(tel);
        }, 1800);
      }

      if (btn) { btn.disabled = true; }
      status.textContent = 'Sending…';

      var request;
      if (files.length) {
        var fd = new FormData();
        Object.keys(payload).forEach(function (k) { fd.append(k, payload[k] == null ? '' : payload[k]); });
        files.forEach(function (f) { fd.append('photos', f, f.name); });
        request = { method: 'POST', body: fd }; // browser sets the multipart boundary
      } else {
        request = {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify(payload)
        };
      }

      fetch('/api/enquiry', request).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          return { ok: res.ok, data: data };
        });
      }).then(function (r) {
        if (btn) { btn.disabled = false; }
        if (r.ok && r.data && r.data.ok) {
          form.reset();
          var n = (r.data && r.data.photos) || 0;
          status.textContent = 'Thanks — that was sent' + (n ? ' with ' + n + (n === 1 ? ' photo' : ' photos') : '') + '. Ben will come back to you shortly.';
          return;
        }
        // not configured, provider error or network: never lose the lead
        status.textContent = 'Opening your email app with the details filled in…';
        mailto();
      }).catch(function () {
        if (btn) { btn.disabled = false; }
        status.textContent = 'Opening your email app with the details filled in…';
        mailto();
      });
    });
  }

  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
