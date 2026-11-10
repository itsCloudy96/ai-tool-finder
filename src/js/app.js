/* Cloudy AI Tool Finder — quiz + directory (no dependencies) */
(function () {
  'use strict';
  var ROOT = document.documentElement.getAttribute('data-root') || './';
  var DATA = null;
  function $(s, el) { return (el || document).querySelector(s); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function load() {
    if (DATA) return Promise.resolve(DATA);
    return fetch(ROOT + 'data/tools.json').then(function (r) { return r.json(); }).then(function (d) { DATA = d; return d; });
  }
  function link(t) { return t.affiliateUrl || t.url; }
  function relFor(t) { return t.affiliateUrl ? 'sponsored noopener' : 'noopener'; }
  function startPrice(t) {
    var m = (t.pricing || '').replace(/,/g, '').match(/\$\s?(\d+(?:\.\d+)?)/g) || [];
    var nums = m.map(function (x) { return parseFloat(x.replace(/[^\d.]/g, '')); }).filter(function (n) { return n > 0; });
    return nums.length ? Math.min.apply(null, nums) : null;
  }
  function style(t) {
    var g = t.tags.join(' ');
    var s = {};
    if (/\bcli\b/.test(g)) s.terminal = 1;
    if (/\bide\b|ide-extension|editor/.test(g)) s.ide = 1;
    if (/sdk|framework|\bapi\b|python|typescript|open-weights|stack/.test(g)) s.code = 1;
    if (/browser|vibe-coding|no-code|low-code|automation|mvp|ui|hosting/.test(g)) s.nocode = 1;
    if (/llm|writing|multi-model|research|search|social|aggregator/.test(g)) s.chat = 1;
    if (!Object.keys(s).length) s.app = 1;
    return s;
  }
  var Q = [
    { id: 'goal', title: 'What do you want AI to help you do?', opts: [
      ['vibe-code', '🚀 Build an app or website (little or no coding)'], ['code', '💻 Write and ship code faster'],
      ['agents', '🤖 Build AI agents or automate workflows'], ['games', '🎮 Make a video game'],
      ['images', '🎨 Create images, art or assets'], ['video', '🎬 Make or edit video'],
      ['audio', '🎵 Music, voice or sound'], ['write', '✍️ Write, chat or brainstorm'],
      ['research', '🔎 Research and get answers with sources'], ['productivity', '🗂️ Meetings, notes, slides and busywork'] ] },
    { id: 'skill', title: 'How technical are you?', opts: [
      ['beginner', 'New to this — keep it simple'], ['intermediate', 'Comfortable — I can follow docs and tinker'], ['advanced', 'Developer — give me power and control'] ] },
    { id: 'budget', title: 'What’s your monthly budget?', opts: [
      ['free', '$0 — free tools only'], ['20', 'Up to ~$20/mo'], ['50', 'Up to ~$50/mo'], ['any', 'Whatever gets the best result'] ] },
    { id: 'style', title: 'Where do you like to work?', opts: [
      ['nocode', 'In the browser, no setup'], ['chat', 'In a chat app'], ['ide', 'Inside a code editor / IDE'],
      ['terminal', 'In the terminal'], ['code', 'In my own code (SDKs, APIs, frameworks)'], ['any', 'No preference'] ] },
    { id: 'priority', title: 'What matters most?', opts: [
      ['ease', 'Easiest to get started'], ['power', 'Best quality / most powerful'], ['open', 'Open source, local or privacy-friendly'], ['value', 'Best value for money'] ] },
    { id: 'context', title: 'Who is this for?', opts: [
      ['hobby', 'Just me — hobby or learning'], ['hustle', 'A side hustle or creator business'], ['team', 'My team or company'] ] }
  ];
  function score(t, a) {
    var s = 0, why = [];
    var ci = t.categories.indexOf(a.goal);
    if (ci === 0) { s += 50; why.push('Built for ' + (DATA.categories[a.goal] || a.goal).toLowerCase()); }
    else if (ci > 0) { s += 32; why.push('Also strong for ' + (DATA.categories[a.goal] || a.goal).toLowerCase()); }
    else return null;
    if (t.skillLevels.indexOf(a.skill) >= 0) { s += 14; why.push('Fits your ' + a.skill + ' skill level'); } else s -= 14;
    var p = startPrice(t);
    if (a.budget === 'free') { if (t.freeTier) { s += 14; why.push('Has a free tier'); } else s -= 40; }
    else if (a.budget === '20') { if (t.freeTier || (p !== null && p <= 20)) { s += 10; why.push(p ? 'Paid plans from ~$' + p : 'Free to start'); } else s -= 12; }
    else if (a.budget === '50') { if (t.freeTier || (p !== null && p <= 50)) s += 8; else s -= 6; }
    var st = style(t);
    if (a.style !== 'any') { if (st[a.style]) { s += 14; why.push(({nocode:'Runs in the browser',chat:'Chat-style interface',ide:'Lives in your editor',terminal:'Terminal-first',code:'Developer SDK / API'})[a.style]); } else if (!st.app) s -= 4; }
    var g = t.tags.join(' ');
    if (a.priority === 'ease' && t.skillLevels.indexOf('beginner') >= 0) { s += 10; why.push('Beginner-friendly'); }
    if (a.priority === 'power' && t.skillLevels.indexOf('advanced') >= 0) { s += 10; why.push('Pro-grade depth'); }
    if (a.priority === 'open' && /open|local|privacy/.test(g)) { s += 14; why.push('Open source / local option'); }
    if (a.priority === 'value' && (t.pricingTier === 'free' || (p !== null && p <= 12))) { s += 10; why.push('Great value'); }
    if (a.context === 'team' && /enterprise|office|microsoft|github|aws/.test(g)) { s += 6; why.push('Team & enterprise features'); }
    if (a.context === 'hustle' && /creative|social|music|video|image|vibe-coding|mvp|hosting/.test(g)) s += 4;
    if (t.featured) s += 3;
    return { t: t, s: s, why: why.slice(0, 4) };
  }
  function recommend(a) {
    return DATA.tools.map(function (t) { return score(t, a); }).filter(Boolean).sort(function (x, y) { return y.s - x.s; }).slice(0, 5);
  }
  function badge(t) {
    var cls = t.pricingTier === 'free' ? 'free' : (t.pricingTier === 'paid' ? 'paid' : '');
    return '<span class="badge ' + cls + '">' + esc(t.pricingTier) + '</span>';
  }
  /* ---------- quiz ---------- */
  function initQuiz() {
    var box = $('#quiz'); if (!box) return;
    var step = 0, ans = {};
    var hash = new URLSearchParams(location.hash.replace(/^#/, ''));
    if (hash.get('goal')) { Q.forEach(function (q) { if (hash.get(q.id)) ans[q.id] = hash.get(q.id); }); if (Object.keys(ans).length === Q.length) step = Q.length; }
    function render() {
      if (step >= Q.length) return results();
      var q = Q[step];
      box.innerHTML = '<div class="progress" aria-hidden="true"><span style="width:' + Math.round(step / Q.length * 100) + '%"></span></div>' +
        '<div class="q-label">Question ' + (step + 1) + ' of ' + Q.length + '</div><h2 class="q-title">' + esc(q.title) + '</h2>' +
        '<div class="options" role="list">' + q.opts.map(function (o) {
          return '<button type="button" class="option' + (ans[q.id] === o[0] ? ' selected' : '') + '" data-v="' + o[0] + '">' + esc(o[1]) + '</button>';
        }).join('') + '</div><div class="quiz-actions">' +
        (step ? '<button type="button" class="btn btn-secondary" id="qback">← Back</button>' : '<span></span>') +
        '<span class="muted" style="align-self:center;font-size:.85rem">Takes ~30 seconds</span></div>';
      box.querySelectorAll('.option').forEach(function (b) { b.addEventListener('click', function () { ans[q.id] = b.getAttribute('data-v'); step++; render(); }); });
      var bk = $('#qback', box); if (bk) bk.addEventListener('click', function () { step--; render(); });
    }
    function results() {
      load().then(function () {
        var r = recommend(ans);
        var qs = new URLSearchParams(ans).toString();
        try { history.replaceState(null, '', '#' + qs); } catch (e) {}
        var share = location.href.split('#')[0] + '#' + qs;
        box.innerHTML = '<div class="progress"><span style="width:100%"></span></div><div class="q-label">Your matches</div>' +
          '<h2 class="q-title">Your top AI tools for ' + esc((DATA.categories[ans.goal] || '').toLowerCase()) + '</h2>' +
          (r.length ? r.map(function (x, i) {
            var t = x.t;
            return '<div class="result-item"><div class="rank">' + (i + 1) + '</div><div style="flex:1"><h3><a href="' + ROOT + 'tool/' + t.id + '/">' + esc(t.name) + '</a></h3>' +
              '<div>' + badge(t) + (t.freeTier ? '<span class="badge free">free tier</span>' : '') + '</div>' +
              '<p class="muted" style="margin:.3rem 0">' + esc(t.bestFor) + '</p><p style="margin:.2rem 0;font-size:.88rem"><strong>Pricing:</strong> ' + esc(t.pricing) + '</p>' +
              '<ul class="why">' + x.why.map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') + '</ul>' +
              '<div class="result-actions"><a class="btn btn-primary btn-sm" href="' + esc(link(t)) + '" target="_blank" rel="' + relFor(t) + '" data-out="' + t.id + '">Try ' + esc(t.name) + ' ↗</a>' +
              '<a class="btn btn-secondary btn-sm" href="' + ROOT + 'tool/' + t.id + '/">Details</a></div></div></div>';
          }).join('') : '<div class="empty">No exact matches — try a bigger budget or “No preference”.</div>') +
          '<div class="share-row"><button class="btn btn-secondary btn-sm" id="qcopy" type="button">🔗 Copy link to these results</button>' +
          '<a class="btn btn-secondary btn-sm" target="_blank" rel="noopener" href="https://x.com/intent/post?text=' + encodeURIComponent('My AI tool stack per Cloudy\'s AI Tool Finder: ' + r.map(function (x) { return x.t.name; }).join(', ') + ' ') + '&url=' + encodeURIComponent(share) + '">Share on X</a>' +
          '<button class="btn btn-secondary btn-sm" id="qagain" type="button">↺ Retake quiz</button>' +
          '<a class="btn btn-secondary btn-sm" href="' + ROOT + 'category/' + esc(ans.goal) + '/">See all ' + esc((DATA.categories[ans.goal] || '').toLowerCase()) + '</a></div>' +
          '<p class="disclaimer">Prices change often — always confirm on the vendor\'s site. Some links may be affiliate links; that never changes our ranking.</p>';
        $('#qagain', box).addEventListener('click', function () { ans = {}; step = 0; try { history.replaceState(null, '', location.pathname); } catch (e) {} render(); });
        $('#qcopy', box).addEventListener('click', function (e) { (navigator.clipboard ? navigator.clipboard.writeText(share) : Promise.reject()).then(function () { e.target.textContent = '✓ Copied'; }, function () { prompt('Copy this link', share); }); });
        box.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    }
    render();
  }
  /* ---------- directory ---------- */
  function initDirectory() {
    var grid = $('#dir-grid'); if (!grid) return;
    load().then(function (d) {
      var q = $('#f-q'), c = $('#f-cat'), p = $('#f-price'), k = $('#f-skill');
      var params = new URLSearchParams(location.search);
      if (params.get('q')) q.value = params.get('q');
      if (params.get('cat')) c.value = params.get('cat');
      function draw() {
        var term = q.value.trim().toLowerCase();
        var list = d.tools.filter(function (t) {
          if (c.value && t.categories.indexOf(c.value) < 0) return false;
          if (p.value === 'free-tier' && !t.freeTier) return false;
          if (p.value && p.value !== 'free-tier' && t.pricingTier !== p.value) return false;
          if (k.value && t.skillLevels.indexOf(k.value) < 0) return false;
          if (term) { var hay = (t.name + ' ' + t.bestFor + ' ' + t.tags.join(' ') + ' ' + t.strengths.join(' ')).toLowerCase(); if (hay.indexOf(term) < 0) return false; }
          return true;
        });
        $('#dir-count').textContent = list.length + ' tool' + (list.length === 1 ? '' : 's');
        grid.innerHTML = list.length ? list.map(function (t) {
          return '<article class="card tool-card"><h3><a href="' + ROOT + 'tool/' + t.id + '/">' + esc(t.name) + '</a></h3><div>' + badge(t) +
            t.categories.slice(0, 2).map(function (x) { return '<span class="badge">' + esc(x) + '</span>'; }).join('') + '</div><p>' + esc(t.bestFor) + '</p>' +
            '<div class="meta"><a href="' + ROOT + 'tool/' + t.id + '/">Details →</a><a href="' + esc(link(t)) + '" target="_blank" rel="' + relFor(t) + '" data-out="' + t.id + '">Visit ↗</a></div></article>';
        }).join('') : '<div class="empty">No tools match those filters.</div>';
      }
      [q, c, p, k].forEach(function (el) { el.addEventListener('input', draw); });
      draw();
    });
  }
  /* newsletter: send to beehiiv subscribe page with email prefilled */
  function initNewsletter() {
    document.querySelectorAll('form.newsletter').forEach(function (f) {
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var em = f.querySelector('input[type=email]').value.trim();
        window.open('https://cloudys-newsletter.beehiiv.com/subscribe' + (em ? '?email=' + encodeURIComponent(em) : ''), '_blank', 'noopener');
      });
    });
  }
  document.addEventListener('DOMContentLoaded', function () { initQuiz(); initDirectory(); initNewsletter(); });
  window.CloudyFinder = { load: load, recommend: function (a) { return load().then(function () { return recommend(a); }); }, questions: Q };
})();
