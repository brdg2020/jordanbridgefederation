# -*- coding: utf-8 -*-
"""HTML + CSS + JS for the "Results" section (Bridgewebs archive), injected by build_site.py.

Kept as plain (non f-string) text so the JavaScript needs no brace escaping.
Data:
  public/data/results/index.json          embedded at build time (event list)
  public/data/results/events/<id>.json    fetched when an event is opened
  public/data/results/players.json        fetched on first player search
"""

RESULTS_SECTION_HTML = r'''
  <!-- SECTION: RESULTS ARCHIVE (migrated from bridgewebs.com/jbf) -->
  <section id="results" class="py-16 bg-gradient-to-b from-slate-100 to-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <div class="flex flex-col lg:flex-row lg:items-end justify-between mb-8 gap-6">
        <div>
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-sky-600"></span>
            <span class="text-xs font-bold uppercase tracking-wider text-sky-800" data-en="Results Archive" data-ar="أرشيف النتائج">Results Archive</span>
          </div>
          <h2 class="text-3xl sm:text-4xl font-black text-slate-900 mt-1 tracking-tight" data-en="Tournament Results 2019 – 2026" data-ar="نتائج البطولات 2019 – 2026">Tournament Results 2019 – 2026</h2>
          <p class="text-sm text-slate-500 mt-2 max-w-2xl" data-en="Rankings, match results, scorecards, travellers, hand records and double-dummy analysis for every event on the federation's results calendar." data-ar="الترتيب ونتائج المباريات وبطاقات النتائج وجداول اللوحات وتوزيعات الأوراق وتحليل Double Dummy لكل بطولات الاتحاد.">Rankings, match results, scorecards, travellers, hand records and double-dummy analysis for every event on the federation's results calendar.</p>
        </div>
        <div class="w-full lg:w-[420px]">
          <label class="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1.5 block" data-en="Find a player" data-ar="ابحث عن لاعب">Find a player</label>
          <div class="relative">
            <i data-lucide="user-search" class="w-5 h-5 text-sky-600 absolute left-3.5 top-3.5"></i>
            <input type="search" id="resPlayerInput" autocomplete="off" oninput="resPlayerSuggest(this.value)" onkeydown="resPlayerKey(event)" placeholder="Type your name…" class="w-full pl-11 pr-4 py-3 text-base bg-white border-2 border-sky-200 rounded-2xl focus:outline-none focus:border-sky-500 shadow-sm">
            <div id="resPlayerList" class="absolute z-30 left-0 right-0 mt-1 bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden hidden"></div>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-3 mb-6">
        <div class="flex flex-col sm:flex-row gap-3 sm:items-center">
          <div class="flex flex-wrap items-center gap-1.5 bg-white p-1.5 rounded-2xl border border-slate-300 shadow-xs w-fit max-w-full" id="resYearBar"></div>
          <div class="relative sm:ml-auto w-full sm:w-64">
            <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-3"></i>
            <input type="search" id="resSearchInput" oninput="resSetSearch(this.value)" placeholder="Filter events…" class="w-full pl-9 pr-3 py-2 text-sm bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500">
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-2" id="resCatBar"></div>
      </div>

      <p class="text-xs text-slate-500 mb-4" id="resCountLine"></p>
      <div id="resListContainer" class="space-y-12"></div>
    </div>
  </section>

  <!-- RESULTS MODAL (event detail / player profile) -->
  <div id="resModal" class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm hidden items-start justify-center p-0 sm:p-4 overflow-y-auto" onclick="if(event.target===this) resClose()">
    <div class="bg-white w-full max-w-7xl sm:rounded-3xl shadow-2xl border border-slate-200 sm:my-4 overflow-hidden min-h-screen sm:min-h-0" id="resModalCard">
      <div class="bg-gradient-to-r from-sky-950 via-sky-900 to-slate-900 text-white px-5 sm:px-8 py-6 relative">
        <div class="absolute top-4 right-4 flex gap-2 res-noprint">
          <button onclick="resPrint()" class="p-2 rounded-full bg-white/10 hover:bg-white/20" title="Print"><i data-lucide="printer" class="w-5 h-5"></i></button>
          <button onclick="resShare()" class="p-2 rounded-full bg-white/10 hover:bg-white/20" title="Copy link"><i data-lucide="link" class="w-5 h-5"></i></button>
          <button onclick="resClose()" class="p-2 rounded-full bg-white/10 hover:bg-white/20" aria-label="Close"><i data-lucide="x" class="w-5 h-5"></i></button>
        </div>
        <p class="text-xs font-bold uppercase tracking-wider text-amber-300" id="resModalMeta"></p>
        <h3 class="text-xl sm:text-3xl font-black mt-1 pr-32" id="resModalTitle"></h3>
        <p class="text-xs text-sky-100/80 mt-2" id="resModalStaff"></p>
      </div>
      <div class="px-4 sm:px-8 pt-5 res-noprint sticky top-0 bg-white/95 backdrop-blur z-20 border-b border-slate-100 pb-3" id="resNavBar">
        <div class="flex flex-wrap gap-2 mb-3" id="resSectionBar"></div>
        <div class="flex flex-wrap gap-1 p-1 bg-slate-100 border border-slate-200 rounded-2xl w-fit max-w-full" id="resTabBar"></div>
      </div>
      <div class="px-4 sm:px-8 py-6" id="resModalBody"></div>
      <div class="px-4 sm:px-8 pb-6 text-[11px] text-slate-400" id="resModalSource"></div>
    </div>
  </div>
  <div id="resToast" class="fixed bottom-6 left-1/2 -translate-x-1/2 z-[60] bg-slate-900 text-white text-sm px-4 py-2 rounded-xl shadow-lg hidden"></div>
'''

RESULTS_CSS = r'''
    .res-pill { transition: all .15s; }
    .res-pill.on { background:#0369a1; color:#fff; border-color:#0369a1; box-shadow:0 1px 3px rgba(3,105,161,.35); }
    .res-tbl { border-collapse: separate; border-spacing:0; width: 100%; font-size: 14px; }
    .res-tbl th, .res-tbl td.h { background:#0f172a; color:#fff; font-weight:700; font-size:11px; text-transform:uppercase; letter-spacing:.04em; padding:9px 10px; text-align:center; white-space:nowrap; position:sticky; top:0; }
    .res-tbl td { padding:8px 10px; border-bottom:1px solid #e2e8f0; text-align:center; white-space:nowrap; }
    .res-tbl td.l { text-align:left; white-space:normal; min-width:170px; }
    .res-tbl tbody tr:nth-child(even) td:not(.h) { background:#f8fafc; }
    .res-tbl tbody tr:hover td:not(.h) { background:#e0f2fe; }
    .res-tbl tr.sel td { background:#fef3c7 !important; }
    .res-tbl tr.click { cursor:pointer; }
    .res-tbl mark { background:#fde68a; color:inherit; border-radius:3px; padding:0 2px; }
    .suit-s, .suit-c { color:#0f172a; } .suit-h, .suit-d { color:#dc2626; }
    .res-hand { display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:10px 14px; align-items:center; }
    .res-seat { font-size:19px; line-height:1.5; font-weight:600; letter-spacing:.02em; white-space:nowrap; }
    .res-seat .sym { display:inline-block; width:1.15em; font-size:1.05em; }
    .res-seat .lbl { font-size:11px; font-weight:800; color:#64748b; text-transform:uppercase; letter-spacing:.08em; }
    .res-hand.sm .res-seat { font-size:15px; line-height:1.4; }
    .res-compass { width:118px; height:118px; border-radius:22px; background:linear-gradient(145deg,#0f172a,#1e3a5f); color:#fff; position:relative; font-weight:800; font-size:12px; margin:auto; box-shadow:0 8px 20px rgba(15,23,42,.25); }
    .res-hand.sm .res-compass { width:88px; height:88px; border-radius:16px; }
    .res-compass span { position:absolute; padding:2px 7px; border-radius:7px; }
    .res-compass .vul { background:#dc2626; } .res-compass .nv { background:#16a34a; }
    .res-compass .n { top:6px; left:50%; transform:translateX(-50%); } .res-compass .s { bottom:6px; left:50%; transform:translateX(-50%); }
    .res-compass .w { left:6px; top:50%; transform:translateY(-50%); } .res-compass .e { right:6px; top:50%; transform:translateY(-50%); }
    .res-compass .bd { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:30px; }
    .res-hand.sm .res-compass .bd { font-size:22px; }
    .res-compass .dl { outline:2px solid #fbbf24; }
    .res-dd td { width:40px; height:30px; text-align:center; font-weight:700; font-size:14px; border:1px solid #e2e8f0; }
    .res-dd td.m { background:#dcfce7; color:#166534; } .res-dd td.x { color:#94a3b8; }
    .res-mx td { padding:4px 6px; font-size:12px; min-width:38px; }
    @media print {
      body > *:not(#resModal) { display:none !important; }
      #resModal { position:static !important; display:block !important; background:none !important; overflow:visible !important; }
      #resModalCard { box-shadow:none !important; border:0 !important; max-width:none !important; }
      .res-noprint { display:none !important; }
      .res-tbl th, .res-tbl td.h { position:static; }
    }
'''

RESULTS_JS = r'''
    // ===================== RESULTS ARCHIVE (Bridgewebs migration) =====================
    const RES = { index: resultsIndex, year: 'all', cat: 'all', q: '', cache: {}, ev: null, sec: 0, tab: 'ranking', board: 0, pair: '', team: 0,
                  players: null, playersLoading: null, hl: '', mode: 'event', profile: null, rankQ: '', lead: null, sugg: [], suggI: -1 };
    const RES_CATS = ['Jordan Bridge Festival', "Jordan Cup", 'Selection & Qualification', 'Other Events'];
    const RES_T = {
      all: ['All', 'الكل'], allYears: ['All years', 'كل السنوات'], events: ['events', 'بطولة'],
      ranking: ['Ranking', 'الترتيب'], matches: ['Matches', 'المباريات'], scorecards: ['Scorecards', 'بطاقات النتائج'],
      travellers: ['Boards', 'اللوحات'], hands: ['Hand records', 'توزيع الأوراق'], matrix: ['Matrix', 'المصفوفة'], ximps: ['X-Imps', 'X-Imps'],
      information: ['Information', 'معلومات'], board: ['Board', 'لوحة'], pair: ['Pair / Team', 'الزوج / الفريق'],
      loading: ['Loading…', 'جارٍ التحميل…'], noData: ['Bridgewebs has no data of this kind for this event.', 'لا تتوفر بيانات من هذا النوع لهذه البطولة على Bridgewebs.'],
      source: ['Source: Bridgewebs results page', 'المصدر: صفحة النتائج على Bridgewebs'], tables: ['tables', 'طاولات'],
      dealer: ['Dealer', 'الموزع'], vul: ['Vul', 'الخطورة'], dd: ['Double dummy: makeable contracts', 'Double Dummy: العقود الممكنة'],
      session: ['Session', 'الجلسة'], vs: ['Opponents', 'الخصوم'], dir: ['Dir', 'الاتجاه'], contract: ['Contract', 'العقد'], by: ['By', 'المنفذ'],
      lead: ['Lead', 'الافتتاح'], tricks: ['Tricks', 'اللمّات'], score: ['Score', 'النتيجة'], points: ['Points', 'النقاط'],
      loadErr: ['Could not load. Please try again.', 'تعذر التحميل. حاول مرة أخرى.'],
      type_Pairs: ['Pairs', 'أزواج'], 'type_Butler Pairs': ['Butler Pairs', 'أزواج (Butler)'], type_Teams: ['Teams', 'فرق'],
      'cat_Jordan Bridge Festival': ['Jordan Bridge Festival', 'مهرجان الأردن للبريدج'], 'cat_Jordan Cup': ["Jordan Cup", 'كأس الأردن'],
      'cat_Selection & Qualification': ['Selection & Qualification', 'التصفيات والاختيار'], 'cat_Other Events': ['Other Events', 'بطولات أخرى'],
      par: ['Par', 'Par'], solver: ['Replay in double-dummy solver', 'إعادة اللعب في محلل Double Dummy'], prev: ['Previous', 'السابق'], next: ['Next', 'التالي'],
      leads: ['Opening leads (double dummy)', 'تحليل الافتتاح (Double Dummy)'], leadHelp: ['Tricks for declarer after each opening lead', 'عدد لمّات المنفذ بعد كل افتتاح'],
      freq: ['Contracts played', 'العقود الملعوبة'], times: ['×', '×'], findInEvent: ['Find a player or pair…', 'ابحث عن لاعب أو زوج…'],
      profile: ['Player history', 'سجل اللاعب'], pos: ['Pos', 'المركز'], event: ['Event', 'البطولة'], partner: ['Partner / Team', 'الشريك / الفريق'],
      noPlayer: ['No player found', 'لم يتم العثور على لاعب'], pbn: ['Download hands (PBN)', 'تحميل التوزيعات (PBN)'], copied: ['Link copied', 'تم نسخ الرابط'],
      pickContract: ['Contract', 'العقد'], declarer: ['Declarer', 'المنفذ'], played: ['played', 'لعب'], resultsFor: ['results', 'نتيجة'],
      ddNote: ['Double-dummy figures computed with the open-source DDS solver; where Bridgewebs published them they match exactly.', 'أرقام Double Dummy محسوبة ببرنامج DDS مفتوح المصدر، وهي مطابقة تمامًا لما نشره Bridgewebs.'],
      none: ['None', 'لا أحد'], ns: ['N/S', 'شمال/جنوب'], ew: ['E/W', 'شرق/غرب'], both: ['All', 'الجميع']
    };
    function rt(k) { const v = RES_T[k]; return v ? v[currentLang === 'ar' ? 1 : 0] : k; }
    function resEsc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
    function resNorm(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9؀-ۿ]+/g, ' ').trim(); }
    function resDate(iso) {
      const d = new Date(iso + 'T12:00:00');
      return d.toLocaleDateString(currentLang === 'ar' ? 'ar-JO' : 'en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    }
    const RES_SUIT = { S: '<span class="suit-s">♠</span>', H: '<span class="suit-h">♥</span>', D: '<span class="suit-d">♦</span>', C: '<span class="suit-c">♣</span>' };
    const RES_STR = ['NT', 'S', 'H', 'D', 'C'];
    function resStrainHtml(s) { return s === 'NT' || s === 'N' ? 'NT' : RES_SUIT[s]; }
    function resSuitText(s) { return resEsc(s).replace(/♠/g, RES_SUIT.S).replace(/♥/g, RES_SUIT.H).replace(/♦/g, RES_SUIT.D).replace(/♣/g, RES_SUIT.C); }
    function resContract(c) {
      if (!c) return '';
      const m = String(c).match(/^([1-7])(NT|N|S|H|D|C)(\*{0,2})(.*)$/);
      if (!m) return resEsc(c);
      const dbl = m[3] === '**' ? 'XX' : (m[3] === '*' ? 'X' : '');
      return '<span class="font-bold">' + m[1] + resStrainHtml(m[2]) + dbl + '</span>' + resEsc(m[4]);
    }
    function resCard(c) {
      if (!c) return '';
      const m = String(c).match(/^([SHDC])(.+)$/);
      return m ? RES_SUIT[m[1]] + resEsc(m[2] === 'T' ? '10' : m[2]) : resEsc(c);
    }
    function resToast(msg) { const t = document.getElementById('resToast'); t.textContent = msg; t.classList.remove('hidden'); clearTimeout(t._h); t._h = setTimeout(() => t.classList.add('hidden'), 1800); }

    // ---------- list ----------
    function resSetSearch(v) { RES.q = v.trim().toLowerCase(); renderResultsList(); }
    function resSetYear(y) { RES.year = y; renderResultsList(); }
    function resSetCat(c) { RES.cat = c; renderResultsList(); }

    function renderResultsList() {
      const evs = RES.index.events;
      const years = [...new Set(evs.map(e => e.year))].sort((a, b) => b - a);
      const pill = (on, label, fn) => `<button onclick="${fn}" class="res-pill ${on ? 'on' : ''} px-3.5 py-1.5 rounded-xl text-xs font-bold border border-transparent text-slate-700 hover:bg-slate-100">${label}</button>`;
      document.getElementById('resYearBar').innerHTML = pill(RES.year === 'all', rt('allYears'), "resSetYear('all')") + years.map(y => pill(RES.year == y, y, `resSetYear(${y})`)).join('');
      const chip = (on, label, n, fn) => `<button onclick="${fn}" class="res-pill ${on ? 'on' : ''} px-3 py-1.5 rounded-full text-xs font-bold bg-white border border-slate-300 text-slate-700 hover:bg-slate-50">${label} <span class="opacity-60">${n}</span></button>`;
      const inYear = evs.filter(e => RES.year === 'all' || e.year == RES.year);
      document.getElementById('resCatBar').innerHTML = chip(RES.cat === 'all', rt('all'), inYear.length, "resSetCat('all')") +
        RES_CATS.filter(c => inYear.some(e => e.category === c)).map(c => chip(RES.cat === c, rt('cat_' + c), inYear.filter(e => e.category === c).length, `resSetCat('${c.replace(/'/g, "\\'")}')`)).join('');
      const list = inYear.filter(e => (RES.cat === 'all' || e.category === RES.cat) &&
        (!RES.q || (e.title + ' ' + e.date + ' ' + e.type + ' ' + e.category + ' ' + (e.staff || []).join(' ')).toLowerCase().includes(RES.q)));
      document.getElementById('resCountLine').textContent = list.length + ' ' + rt('events');
      const catColor = { 'Jordan Bridge Festival': 'from-amber-400 to-orange-500', 'Jordan Cup': 'from-emerald-500 to-teal-600', 'Selection & Qualification': 'from-sky-500 to-indigo-600', 'Other Events': 'from-fuchsia-500 to-rose-500' };
      const out = [];
      years.forEach(y => {
        const ye = list.filter(e => e.year === y);
        if (!ye.length) return;
        out.push(`<div><div class="flex items-center gap-3 mb-5"><h3 class="text-3xl font-black text-slate-900">${y}</h3><span class="h-px flex-1 bg-slate-300"></span><span class="text-xs font-bold text-slate-500">${ye.length} ${rt('events')}</span></div>`);
        RES_CATS.forEach(c => {
          const ce = ye.filter(e => e.category === c);
          if (!ce.length) return;
          out.push(`<p class="text-xs font-bold uppercase tracking-wider text-sky-800 mb-3 mt-5">${rt('cat_' + c)}</p><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">`);
          ce.forEach(e => {
            const tags = [rt('ranking')];
            if (e.travellers) tags.push(rt('scorecards'), rt('travellers'));
            if (e.dd) tags.push('Double dummy');
            if (e.matches) tags.push(rt('matches'));
            const d = new Date(e.date + 'T12:00:00');
            out.push(`<button onclick="resOpenEvent('${e.id}')" class="text-left bg-white rounded-2xl border border-slate-200 hover:border-sky-400 hover:shadow-lg hover:-translate-y-0.5 transition-all overflow-hidden flex group">
              <div class="w-16 shrink-0 bg-gradient-to-b ${catColor[e.category] || 'from-slate-400 to-slate-600'} text-white flex flex-col items-center justify-center py-3">
                <span class="text-2xl font-black leading-none">${d.getDate()}</span>
                <span class="text-[10px] font-bold uppercase tracking-wider mt-1">${d.toLocaleDateString('en-GB', { month: 'short' })}</span>
              </div>
              <div class="p-4 flex flex-col gap-1.5 min-w-0 flex-1">
                <div class="flex items-center justify-between gap-2">
                  <span class="text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full ${e.type === 'Teams' ? 'bg-emerald-100 text-emerald-800' : (e.type === 'Butler Pairs' ? 'bg-amber-100 text-amber-800' : 'bg-sky-100 text-sky-800')}">${rt('type_' + e.type)}</span>
                  <span class="text-[11px] text-slate-400">${e.tables ? resEsc(e.tables) + ' ' + rt('tables') : ''}</span>
                </div>
                <span class="font-extrabold text-slate-900 leading-snug group-hover:text-sky-800">${resEsc(e.title)}</span>
                ${e.winner ? `<span class="text-xs text-slate-600 flex items-center gap-1 min-w-0"><span class="text-amber-500">🏆</span><span class="truncate font-semibold">${resEsc(e.winner)}</span></span>` : ''}
                ${(e.staff || []).length ? `<span class="text-[11px] text-slate-500 truncate">${resEsc(e.staff.join(' · '))}</span>` : ''}
                <span class="flex flex-wrap gap-1 mt-1">${tags.map(t => `<span class="text-[10px] font-semibold px-1.5 py-0.5 rounded-md bg-slate-100 text-slate-600">${t}</span>`).join('')}</span>
              </div>
            </button>`);
          });
          out.push('</div>');
        });
        out.push('</div>');
      });
      document.getElementById('resListContainer').innerHTML = out.join('') || `<p class="text-sm text-slate-500">–</p>`;
      const pi = document.getElementById('resPlayerInput'); if (pi) pi.placeholder = currentLang === 'ar' ? 'اكتب اسمك…' : 'Type your name…';
      const si = document.getElementById('resSearchInput'); if (si) si.placeholder = currentLang === 'ar' ? 'تصفية البطولات…' : 'Filter events…';
    }

    // ---------- player search ----------
    async function resLoadPlayers() {
      if (RES.players) return RES.players;
      if (!RES.playersLoading) RES.playersLoading = fetch('public/data/results/players.json').then(r => r.json()).then(d => { RES.players = d.players; return RES.players; });
      return RES.playersLoading;
    }
    async function resPlayerSuggest(v) {
      const box = document.getElementById('resPlayerList');
      const q = resNorm(v);
      if (q.length < 2) { box.classList.add('hidden'); return; }
      const ps = await resLoadPlayers();
      const words = q.split(' ');
      const hits = ps.filter(p => words.every(w => p.k.includes(w))).sort((a, b) => b.e.length - a.e.length).slice(0, 12);
      RES.sugg = hits; RES.suggI = -1;
      box.innerHTML = hits.length ? hits.map((p, i) => `<button onmousedown="resOpenPlayer('${resEsc(p.k)}')" data-i="${i}" class="w-full text-left px-4 py-2.5 hover:bg-sky-50 flex items-center justify-between gap-3 border-b border-slate-100 last:border-0">
          <span class="font-semibold text-slate-800">${resEsc(p.n)}</span><span class="text-xs text-slate-400 shrink-0">${p.e.length} ${rt('resultsFor')}</span></button>`).join('')
        : `<p class="px-4 py-3 text-sm text-slate-500">${rt('noPlayer')}</p>`;
      box.classList.remove('hidden');
    }
    function resPlayerKey(e) {
      const box = document.getElementById('resPlayerList');
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        RES.suggI = Math.max(0, Math.min(RES.sugg.length - 1, RES.suggI + (e.key === 'ArrowDown' ? 1 : -1)));
        box.querySelectorAll('button').forEach((b, i) => b.classList.toggle('bg-sky-50', i === RES.suggI));
      } else if (e.key === 'Enter') {
        const p = RES.sugg[RES.suggI >= 0 ? RES.suggI : 0]; if (p) resOpenPlayer(p.k);
      } else if (e.key === 'Escape') box.classList.add('hidden');
    }
    document.addEventListener('click', e => { if (!e.target.closest('#resPlayerList') && e.target.id !== 'resPlayerInput') { const b = document.getElementById('resPlayerList'); if (b) b.classList.add('hidden'); } });

    async function resOpenPlayer(key) {
      document.getElementById('resPlayerList').classList.add('hidden');
      const ps = await resLoadPlayers();
      const p = ps.find(x => x.k === key);
      if (!p) return;
      RES.mode = 'player'; RES.profile = p; RES.hl = key; RES.ev = null;
      resShowModal();
      history.replaceState(null, '', '#results/player/' + encodeURIComponent(key));
      document.getElementById('resModalMeta').textContent = rt('profile');
      document.getElementById('resModalTitle').textContent = p.n;
      document.getElementById('resModalStaff').textContent = p.e.length + ' ' + rt('resultsFor');
      document.getElementById('resSectionBar').innerHTML = '';
      document.getElementById('resTabBar').innerHTML = '';
      document.getElementById('resModalSource').innerHTML = '';
      const byId = {}; RES.index.events.forEach(e => byId[e.id] = e);
      const rows = p.e.slice().sort((a, b) => b[0].localeCompare(a[0]));
      const years = [...new Set(rows.map(r => r[0].slice(0, 4)))];
      let html = '';
      years.forEach(y => {
        html += `<h4 class="text-xl font-black text-slate-900 mt-6 mb-3">${y}</h4><div class="overflow-x-auto rounded-2xl border border-slate-200"><table class="res-tbl"><thead><tr><th>${rt('pos')}</th><th>${rt('event')}</th><th>${rt('partner')}</th><th>${rt('score')}</th></tr></thead><tbody>`;
        rows.filter(r => r[0].startsWith(y)).forEach(r => {
          const ev = byId[r[0]] || {};
          const top = /^[123]=?$/.test(r[2]) ? `<span class="badge-rank-${r[2][0]} inline-flex items-center justify-center min-w-7 h-7 px-1.5 rounded-full text-xs font-black">${resEsc(r[2])}</span>` : `<span class="font-bold">${resEsc(r[2])}</span>`;
          html += `<tr class="click" onclick="resOpenEvent('${r[0]}', {sec:${r[1]}, pair:'${resEsc(r[5])}', tab:'${ev.travellers ? 'scorecards' : 'ranking'}', hl:'${resEsc(p.k)}'})">
            <td>${top}</td><td class="l"><div class="font-bold text-slate-900">${resEsc(ev.title || r[0])}</div><div class="text-xs text-slate-500">${ev.date ? resDate(ev.date) : ''}${ev.sections && ev.sections.length && r[1] ? ' · ' + resEsc(ev.sections[r[1]] || '') : ''}</div></td>
            <td class="l">${r[6] ? '<span class="font-semibold">' + resEsc(r[6]) + '</span><br>' : ''}<span class="text-slate-600 text-sm">${resEsc(r[7])}</span></td>
            <td><span class="font-mono font-bold">${resEsc(r[3])}</span><div class="text-[10px] text-slate-400">${resEsc(r[4])}</div></td></tr>`;
        });
        html += '</tbody></table></div>';
      });
      document.getElementById('resModalBody').innerHTML = html;
      lucide.createIcons();
    }

    // ---------- modal / routing ----------
    function resShowModal() {
      const modal = document.getElementById('resModal');
      modal.classList.remove('hidden'); modal.classList.add('flex');
      document.body.style.overflow = 'hidden';
    }
    function resClose() {
      const modal = document.getElementById('resModal');
      modal.classList.add('hidden'); modal.classList.remove('flex');
      document.body.style.overflow = '';
      RES.ev = null; RES.mode = 'event';
      if (location.hash.startsWith('#results/')) history.replaceState(null, '', '#results');
    }
    function resHash() {
      if (RES.mode === 'player' && RES.profile) return '#results/player/' + encodeURIComponent(RES.profile.k);
      if (!RES.ev) return '#results';
      let h = '#results/' + RES.ev.id + '/' + RES.sec + '/' + RES.tab;
      if (RES.tab === 'travellers') h += '/' + RES.board;
      if (RES.tab === 'scorecards' && RES.pair) h += '/' + encodeURIComponent(RES.pair);
      return h;
    }
    function resSyncHash() { const h = resHash(); if (location.hash !== h) history.replaceState(null, '', h); }
    function resShare() {
      const url = location.origin + location.pathname + resHash();
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(() => resToast(rt('copied'))).catch(() => prompt('URL', url));
    }
    function resPrint() { window.print(); }
    document.addEventListener('keydown', e => {
      if (document.getElementById('resModal').classList.contains('hidden')) return;
      if (e.key === 'Escape') resClose();
      if (RES.ev && RES.tab === 'travellers' && !/INPUT|SELECT|TEXTAREA/.test((e.target || {}).tagName || '')) {
        const n = (resSection().boards || []).length;
        if (e.key === 'ArrowRight' && RES.board < n - 1) resGoBoard(RES.board + 1);
        if (e.key === 'ArrowLeft' && RES.board > 0) resGoBoard(RES.board - 1);
      }
    });

    async function resOpenEvent(id, opts) {
      opts = opts || {};
      const meta = RES.index.events.find(e => e.id === id);
      if (!meta) return;
      RES.mode = 'event';
      resShowModal();
      document.getElementById('resModalMeta').textContent = resDate(meta.date) + ' · ' + rt('cat_' + meta.category) + ' · ' + rt('type_' + meta.type);
      document.getElementById('resModalTitle').textContent = meta.title;
      document.getElementById('resModalStaff').textContent = [meta.tables ? meta.tables + ' ' + rt('tables') : ''].concat(meta.staff || []).filter(Boolean).join(' · ');
      RES.sec = opts.sec || 0; RES.tab = opts.tab || 'ranking'; RES.board = opts.board || 0; RES.pair = opts.pair || ''; RES.team = 0; RES.rankQ = ''; RES.lead = null;
      RES.hl = opts.hl || ''; RES.hlDone = false;
      if (!RES.cache[id]) {
        document.getElementById('resSectionBar').innerHTML = '';
        document.getElementById('resTabBar').innerHTML = '';
        document.getElementById('resModalBody').innerHTML = `<p class="text-sm text-slate-500">${rt('loading')}</p>`;
        try {
          const r = await fetch('public/data/results/events/' + id + '.json');
          if (!r.ok) throw new Error(r.status);
          RES.cache[id] = await r.json();
        } catch (err) {
          document.getElementById('resModalBody').innerHTML = `<p class="text-sm text-red-600">${rt('loadErr')}</p>`;
          return;
        }
      }
      RES.ev = RES.cache[id];
      document.getElementById('resModalSource').innerHTML = `${rt('source')}: <a class="underline hover:text-sky-700" href="${RES.ev.source}" target="_blank" rel="noopener">${resEsc(RES.ev.source)}</a>`;
      resRenderEvent();
      document.getElementById('resModal').scrollTop = 0;
    }

    function resSection() { return RES.ev.sections[RES.sec] || RES.ev.sections[0]; }
    function resHasTrav(s) { return (s.boards || []).some(b => b.rows && b.rows.length); }
    function resTabsFor(s) {
      const t = ['ranking'];
      if (s.matches && s.matches.length) t.push('matches');
      const trav = resHasTrav(s);
      if (trav && s.pairs && s.pairs.length) t.push('scorecards');
      if (trav || (s.boards || []).some(b => b.hands)) t.push('travellers');
      if (trav && s.pairs && s.pairs.length && RES.ev.type !== 'Teams') t.push('matrix');
      if ((s.boards || []).some(b => b.hands)) t.push('hands');
      if (s.ximps && s.ximps.length) t.push('ximps');
      if (s.information) t.push('information');
      return t;
    }
    function resSetSec(i) { RES.sec = i; RES.board = 0; RES.pair = ''; RES.team = 0; const t = resTabsFor(resSection()); if (!t.includes(RES.tab)) RES.tab = 'ranking'; resRenderEvent(); }
    function resSetTab(t) { RES.tab = t; resRenderEvent(); document.getElementById('resNavBar').scrollIntoView({ block: 'nearest' }); }

    function resRenderEvent() {
      if (!RES.ev) return;
      const ev = RES.ev, s = resSection();
      document.getElementById('resSectionBar').innerHTML = ev.sections.length > 1 ? ev.sections.map((x, i) =>
        `<button onclick="resSetSec(${i})" class="res-pill ${i === RES.sec ? 'on' : ''} px-3 py-1.5 rounded-full text-xs font-bold bg-white border border-slate-300 text-slate-700">${resEsc(x.label || (rt('session') + ' ' + (i + 1)))}</button>`).join('') : '';
      const tabs = resTabsFor(s);
      if (!tabs.includes(RES.tab)) RES.tab = 'ranking';
      const hasHands = (s.boards || []).some(b => b.hands);
      document.getElementById('resTabBar').innerHTML = tabs.map(t =>
        `<button onclick="resSetTab('${t}')" class="res-pill ${t === RES.tab ? 'on' : ''} px-4 py-2 rounded-xl text-xs sm:text-sm font-bold text-slate-700 hover:bg-white">${rt(t)}</button>`).join('') +
        (hasHands ? `<button onclick="resDownloadPBN()" class="px-3 py-2 rounded-xl text-xs font-bold text-sky-700 hover:bg-white flex items-center gap-1" title="${rt('pbn')}"><i data-lucide="download" class="w-4 h-4"></i>PBN</button>` : '');
      const fn = { ranking: resRenderRanking, matches: resRenderMatches, scorecards: resRenderScorecards, travellers: resRenderBoards, hands: resRenderHands, matrix: resRenderMatrix, ximps: resRenderXimps, information: resRenderInfo }[RES.tab];
      const tabBefore = RES.tab;
      document.getElementById('resModalBody').innerHTML = fn(s);
      if (RES.tab !== tabBefore) return resRenderEvent();
      resSyncHash();
      lucide.createIcons();
    }

    // generic Bridgewebs table (cells: {t, cs, rs, h})
    function resRowMatches(r, q) { if (!q) return false; return resNorm(r.map(c => c.t).join(' ')).includes(q); }
    function resGenericTable(rows, opts) {
      opts = opts || {};
      const q = resNorm(RES.rankQ), hl = RES.hl;
      const html = ['<div class="overflow-x-auto rounded-2xl border border-slate-200 shadow-xs"><table class="res-tbl"><tbody>'];
      let direction = '';
      rows.forEach(r => {
        if (r.length === 1 && r[0].h) { const t = r[0].t.toLowerCase(); direction = t.includes('north') ? 'NS' : (t.includes('east') ? 'EW' : direction); }
        const isHead = r.some(c => c.h);
        if (!isHead && q && opts.filter && !resRowMatches(r, q)) return;
        const sel = !isHead && ((hl && resNorm(r.map(c => c.t).join(' ')).includes(hl)) || (q && resRowMatches(r, q)));
        let click = '';
        if (!isHead && opts.rowLink) {
          const key = opts.rowLink(r, direction);
          if (key) click = ` class="click ${sel ? 'sel' : ''}" onclick="RES.pair='${resEsc(key)}';resSetTab('scorecards')"`;
        }
        html.push(click ? `<tr${click}>` : `<tr class="${sel ? 'sel' : ''}">`);
        r.forEach((c, ci) => {
          const attrs = (c.cs ? ` colspan="${c.cs}"` : '') + (c.rs ? ` rowspan="${c.rs}"` : '');
          const txt = c.t || '';
          let inner = resSuitText(txt).replace(/\n/g, '<br>');
          if (!c.h && opts.rankCol === ci && /^[123]=?$/.test(txt)) inner = `<span class="badge-rank-${txt[0]} inline-flex items-center justify-center min-w-8 h-8 px-1.5 rounded-full text-sm font-black">${resEsc(txt)}</span>`;
          const cls = c.h ? 'h' : (txt.length > 18 || txt.includes('\n') ? 'l' : '');
          html.push(`<td class="${cls}"${attrs}>${inner}</td>`);
        });
        html.push('</tr>');
      });
      html.push('</tbody></table></div>');
      return html.join('');
    }
    function resNoData() { return `<div class="text-center py-10"><p class="text-sm text-slate-500">${rt('noData')}</p></div>`; }
    function resFindBox(ph) {
      return `<div class="relative w-full sm:w-80 mb-4 res-noprint"><i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-3"></i>
        <input type="search" value="${resEsc(RES.rankQ)}" oninput="RES.rankQ=this.value;resRerenderKeepFocus(this)" placeholder="${ph}" class="w-full pl-9 pr-3 py-2 text-sm bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500"></div>`;
    }
    function resRerenderKeepFocus(inp) {
      const pos = inp.selectionStart; resRenderEvent();
      const n = document.querySelector('#resModalBody input[type=search]'); if (n) { n.focus(); try { n.setSelectionRange(pos, pos); } catch (e) {} }
    }

    function resRenderRanking(s) {
      const rk = s.ranking || {};
      const trav = resHasTrav(s) && s.pairs && s.pairs.length;
      const opts = { rankCol: 0, filter: true };
      if (trav) {
        const po = resScorecardOptions(s);
        opts.rowLink = (r, dir) => {
          const txt = resNorm(r.map(c => c.t).join(' '));
          // the pair (or first pair of a team) whose player names appear in the row
          const hit = po.find(o => { const ns = o.names.split(' & ').map(resNorm).filter(x => x.length > 1); return ns.length && ns.every(n => txt.includes(n)); });
          if (hit) return hit.key;
          const no = (r[1] || {}).t; if (!no || !/^\d+$/.test(no)) return '';
          const k = (dir ? dir : '') + ':' + no;
          return po.find(o => o.key === k) ? k : '';
        };
      }
      const parts = [resFindBox(rt('findInEvent'))];
      (rk.tables || []).forEach(t => parts.push(resGenericTable(t, opts)));
      if (rk.info && rk.info.length) {
        parts.push('<dl class="mt-6 grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-1 text-xs text-slate-600 bg-slate-50 rounded-2xl p-4">' +
          rk.info.map(kv => `<div class="flex gap-2"><dt class="font-bold text-slate-500 min-w-36">${resEsc(kv[0])}</dt><dd>${resEsc(kv[1])}</dd></div>`).join('') + '</dl>');
      }
      return parts.join('') || resNoData();
    }

    function resRenderMatches(s) {
      const m = s.matches || [];
      if (!m.length) return resNoData();
      const i = Math.min(RES.team, m.length - 1);
      const bar = '<div class="flex flex-wrap gap-2 mb-4">' + m.map((x, k) =>
        `<button onclick="RES.team=${k};resRenderEvent()" class="res-pill ${k === i ? 'on' : ''} px-3 py-1.5 rounded-full text-xs font-bold bg-white border border-slate-300 text-slate-700">${resEsc(x.team || ('#' + (k + 1)))}</button>`).join('') + '</div>';
      return bar + m[i].tables.map(t => resGenericTable(t)).join('<div class="h-4"></div>');
    }
    function resRenderXimps(s) { return (s.ximps || []).map(t => resGenericTable(t, { rankCol: 0 })).join('<div class="h-4"></div>') || resNoData(); }
    function resRenderInfo(s) {
      const inf = s.information || {};
      const t = (inf.tables || []).map(x => resGenericTable(x)).join('<div class="h-4"></div>');
      return t || (inf.text ? `<div class="text-sm text-slate-700 whitespace-pre-line">${resEsc(inf.text)}</div>` : resNoData());
    }

    // ---- pairs ----
    function resPairMaps(s) {
      if (s._pm) return s._pm;
      const mitchell = (s.pairs || []).some(p => p.way === '2');
      const ns = {}, ew = {};
      (s.pairs || []).forEach(p => {
        const nm = p.names.filter(Boolean).join(' & ');
        if (mitchell) { (p.way === '2' ? ew : ns)[p.pair] = nm; } else { ns[p.pair] = nm; ew[p.pair] = nm; }
      });
      s._pm = { mitchell, ns, ew };
      return s._pm;
    }
    function resScorecardOptions(s) {
      if (s._opts) return s._opts;
      const pm = resPairMaps(s);
      const seenNS = new Set(), seenEW = new Set();
      (s.boards || []).forEach(b => { const c = b.cols || [], i = c.indexOf('NS'), j = c.indexOf('EW'); (b.rows || []).forEach(r => { seenNS.add(r[i]); seenEW.add(r[j]); }); });
      const opts = [];
      (s.pairs || []).forEach(p => {
        const dir = pm.mitchell ? (p.way === '2' ? 'EW' : 'NS') : '';
        if (dir === 'NS' ? !seenNS.has(p.pair) : dir === 'EW' ? !seenEW.has(p.pair) : !(seenNS.has(p.pair) || seenEW.has(p.pair))) return;
        const names = p.names.filter(Boolean).join(' & ');
        opts.push({ key: dir + ':' + p.pair, no: p.pair, dir, names, label: (dir ? dir + ' ' : '') + p.pair + ' — ' + names });
      });
      s._opts = opts;
      return opts;
    }
    // one row per board for a pair, taken from the travellers
    function resPairLines(s, cur) {
      const pm = resPairMaps(s);
      const lines = [];
      (s.boards || []).forEach((b, bi) => {
        const cols = b.cols || []; const iNS = cols.indexOf('NS'), iEW = cols.indexOf('EW');
        (b.rows || []).forEach(r => {
          let dir = null;
          if (cur.dir !== 'EW' && r[iNS] === cur.no) dir = 'NS';
          else if (cur.dir !== 'NS' && r[iEW] === cur.no) dir = 'EW';
          if (!dir) return;
          const g = k => { const i = cols.indexOf(k); return i >= 0 ? r[i] : ''; };
          const opp = dir === 'NS' ? r[iEW] : r[iNS];
          const plus = g('+Sc'), minus = g('-Sc');
          let sc = '';
          if (dir === 'NS') sc = plus && plus !== '-' ? plus : (minus && minus !== '-' ? '−' + minus : (plus || minus));
          else sc = minus && minus !== '-' ? minus : (plus && plus !== '-' ? '−' + plus : (plus || minus));
          lines.push({ bi, b, dir, opp, oppName: (dir === 'NS' ? pm.ew : pm.ns)[opp] || '', bid: g('Bid'), by: g('By'), ld: g('Ld'), tks: g('Tks'), sc, pts: dir === 'NS' ? r[cols.length - 2] : r[cols.length - 1] });
        });
      });
      return lines;
    }
    function resPairPicker(s, onchange) {
      const opts = resScorecardOptions(s);
      const cur = opts.find(o => o.key === RES.pair) || opts[0];
      return `<div class="mb-5 flex flex-col sm:flex-row sm:items-center gap-3 res-noprint">
        <div class="relative w-full sm:w-96"><i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-3.5"></i>
          <input list="resPairList" placeholder="${rt('findInEvent')}" class="w-full pl-9 pr-3 py-2.5 text-sm bg-white border-2 border-sky-200 rounded-xl focus:outline-none focus:border-sky-500"
            onchange="const o=resScorecardOptions(resSection()).find(x=>x.label===this.value); if(o){RES.pair=o.key;${onchange}}">
          <datalist id="resPairList">${opts.map(o => `<option value="${resEsc(o.label)}"></option>`).join('')}</datalist></div>
        <select onchange="RES.pair=this.value;${onchange}" class="text-sm p-2.5 border border-slate-300 rounded-xl bg-white max-w-full">${opts.map(o => `<option value="${resEsc(o.key)}" ${cur && o.key === cur.key ? 'selected' : ''}>${resEsc(o.label)}</option>`).join('')}</select>
      </div>`;
    }
    function resRenderScorecards(s) {
      const opts = resScorecardOptions(s);
      if (!opts.length) return resNoData();
      if (RES.hl && !RES.hlDone) {
        RES.hlDone = true;
        const byName = opts.find(o => resNorm(o.names).includes(RES.hl));
        if (byName) RES.pair = byName.key;
        else { RES.tab = 'ranking'; return resRenderRanking(s); }   // the player has no traveller lines here
      }
      if (!opts.find(o => o.key === RES.pair)) {
        // links from the ranking or a player profile: prefer the pair holding the searched player, then the number
        const byName = RES.hl ? opts.find(o => resNorm(o.names).includes(RES.hl)) : null;
        const no = (RES.pair || '').split(':').pop();
        const alt = byName || opts.find(o => o.no === no);
        RES.pair = alt ? alt.key : opts[0].key;
      }
      const cur = opts.find(o => o.key === RES.pair);
      const lines = resPairLines(s, cur);
      const multiSess = (s.boards || []).some(x => x.sess !== (s.boards[0] || {}).sess);
      const hasLd = (s.boards || []).some(b => (b.cols || []).includes('Ld'));
      const head = `<tr><th>${rt('board')}</th>${multiSess ? `<th>${rt('session')}</th>` : ''}<th>${rt('dir')}</th><th>${rt('vs')}</th><th>${rt('contract')}</th><th>${rt('by')}</th>${hasLd ? `<th>${rt('lead')}</th>` : ''}<th>${rt('tricks')}</th><th>${rt('score')}</th><th>${rt('points')}</th><th>${rt('par')}</th></tr>`;
      let total = 0, numeric = true;
      const body = lines.map(L => {
        const v = parseFloat(String(L.pts).replace('+', '')); if (isNaN(v)) numeric = false; else total += v;
        const par = L.b.dds ? (L.dir === 'NS' ? L.b.dds.par : -L.b.dds.par) : '';
        return `<tr class="click" onclick="RES.board=${L.bi};RES.tab='travellers';resRenderEvent()"><td><span class="font-bold text-sky-700 underline">${resEsc(L.b.bd)}</span></td>${multiSess ? `<td>${resEsc(L.b.sess)}</td>` : ''}<td>${L.dir === 'NS' ? 'N/S' : 'E/W'}</td>
          <td class="l"><span class="font-bold">${resEsc(L.opp)}</span> <span class="text-xs text-slate-500">${resEsc(L.oppName)}</span></td>
          <td>${resContract(L.bid)}</td><td>${resEsc(L.by)}</td>${hasLd ? `<td>${resCard(L.ld)}</td>` : ''}<td>${resEsc(L.tks)}</td><td class="font-mono">${resEsc(L.sc)}</td><td class="font-bold font-mono">${resEsc(L.pts)}</td><td class="text-xs text-slate-500 font-mono">${par === '' ? '' : (par > 0 ? '+' : '') + par}</td></tr>`;
      }).join('');
      const summary = `<div class="flex flex-wrap items-center gap-3 mb-4"><div class="bg-gradient-to-r from-sky-50 to-white border border-sky-100 rounded-2xl px-5 py-3">
          <div class="text-[11px] font-bold uppercase tracking-wider text-sky-700">${resEsc(cur.dir ? cur.dir + ' ' : '')}${resEsc(cur.no)}</div>
          <div class="text-lg font-black text-slate-900">${resEsc(cur.names)}</div></div>
          ${numeric && lines.length ? `<div class="bg-slate-50 border border-slate-200 rounded-2xl px-5 py-3"><div class="text-[11px] font-bold uppercase tracking-wider text-slate-500">${rt('points')} Σ</div><div class="text-lg font-black font-mono">${Math.round(total * 100) / 100}</div></div>` : ''}</div>`;
      return resPairPicker(s, 'resRenderEvent()') + summary + (lines.length ? `<div class="overflow-x-auto rounded-2xl border border-slate-200 shadow-xs"><table class="res-tbl"><thead>${head}</thead><tbody>${body}</tbody></table></div>` : resNoData());
    }

    // ---- matrix: every pair's points on every board ----
    function resRenderMatrix(s) {
      const opts = resScorecardOptions(s);
      if (!opts.length) return resNoData();
      const boards = s.boards || [];
      const q = resNorm(RES.rankQ);
      const data = opts.map(o => { const m = {}; resPairLines(s, o).forEach(L => m[L.bi] = L.pts); return { o, m }; });
      const ranges = boards.map((b, bi) => { const v = data.map(d => parseFloat(d.m[bi])).filter(x => !isNaN(x)); return v.length ? [Math.min(...v), Math.max(...v)] : [0, 0]; });
      const col = (v, bi) => { const x = parseFloat(v); if (isNaN(x)) return ''; const [lo, hi] = ranges[bi]; if (hi === lo) return ''; const t = (x - lo) / (hi - lo); const h = Math.round(t * 120); return `background:hsl(${h},70%,${92 - Math.abs(t - .5) * 16}%)`; };
      let html = resFindBox(rt('findInEvent')) + '<div class="overflow-auto rounded-2xl border border-slate-200 max-h-[70vh]"><table class="res-tbl res-mx"><thead><tr><th class="sticky left-0 z-10">' + rt('pair') + '</th>' +
        boards.map((b, bi) => `<th class="cursor-pointer" onclick="resGoBoard(${bi});RES.tab='travellers';resRenderEvent()">${resEsc(b.bd)}</th>`).join('') + '</tr></thead><tbody>';
      data.forEach(d => {
        if (q && !resNorm(d.o.label).includes(q)) return;
        const sel = RES.hl && resNorm(d.o.names).includes(RES.hl);
        html += `<tr class="${sel ? 'sel' : ''}"><td class="l sticky left-0 bg-white z-[1] cursor-pointer" onclick="RES.pair='${resEsc(d.o.key)}';resSetTab('scorecards')"><span class="font-bold">${resEsc(d.o.dir ? d.o.dir + ' ' : '')}${resEsc(d.o.no)}</span> <span class="text-xs text-slate-500">${resEsc(d.o.names)}</span></td>` +
          boards.map((b, bi) => `<td style="${col(d.m[bi], bi)}">${resEsc(d.m[bi] === undefined ? '' : d.m[bi])}</td>`).join('') + '</tr>';
      });
      return html + '</tbody></table></div>';
    }

    // ---- hand diagram ----
    function resSeat(b, seat, cls) {
      const h = b.hands[seat];
      const lines = ['S', 'H', 'D', 'C'].map((st, i) => `<div><span class="sym">${RES_SUIT[st]}</span>${h[i] ? resEsc(h[i].replace(/T/g, '10').split('').join(' ').replace(/1 0/g, '10')) : '<span class="text-slate-300">—</span>'}</div>`).join('');
      return `<div class="res-seat ${cls || ''}"><div class="lbl">${seat}${b.hcp && b.hcp[seat] ? ' · ' + resEsc(b.hcp[seat]) + ' HCP' : ''}</div>${lines}</div>`;
    }
    function resCompass(b) {
      const nsV = b.vul === 'NS' || b.vul === 'All', ewV = b.vul === 'EW' || b.vul === 'All';
      const sp = (k, v) => `<span class="${k} ${v ? 'vul' : 'nv'} ${b.dealer === k.toUpperCase() ? 'dl' : ''}" title="${b.dealer === k.toUpperCase() ? rt('dealer') : ''}">${k.toUpperCase()}</span>`;
      return `<div class="res-compass">${sp('n', nsV)}${sp('s', nsV)}${sp('w', ewV)}${sp('e', ewV)}<div class="bd">${resEsc(b.bd)}</div></div>`;
    }
    function resDDTricks(b) {
      // returns {seat:{strain:tricks}} from the solver or, failing that, Bridgewebs' own figures
      if (b.dds) { const o = {}; 'NESW'.split('').forEach((p, pi) => { o[p] = {}; RES_STR.forEach((st, si) => o[p][st] = b.dds.t[si][pi]); }); return o; }
      if (b.dd) { const o = {}; 'NESW'.split('').forEach(p => { o[p] = {}; RES_STR.forEach(st => { const v = parseInt((b.dd[p] || {})[st], 10); o[p][st] = isNaN(v) ? null : v; }); }); return o; }
      return null;
    }
    function resDDTable(b) {
      const tr = resDDTricks(b);
      let rows = '';
      const cols = ['NT', 'S', 'H', 'D', 'C'];
      if (tr) {
        rows = ['N', 'S', 'E', 'W'].map(p => `<tr><td class="font-black text-slate-500 border-0">${p}</td>${cols.map(c => { const t = tr[p][c]; if (t === null || t === undefined) return '<td></td>'; return `<td class="${t > 6 ? 'm' : 'x'}" title="${t} ${rt('tricks')}">${t > 6 ? t - 6 : '–'}</td>`; }).join('')}</tr>`).join('');
      } else if (b.ddl) {
        rows = ['N', 'S', 'E', 'W'].filter(p => b.ddl[p]).map(p => `<tr><td class="font-black text-slate-500 border-0">${p}</td>${cols.map(c => { const v = b.ddl[p][c] || ''; return `<td class="${v && v !== '-' ? 'm' : 'x'}">${resEsc(v === '-' ? '–' : v)}</td>`; }).join('')}</tr>`).join('');
      } else return '';
      const par = b.dds ? `<div class="mt-3 text-sm"><span class="font-black text-slate-700">${rt('par')}:</span> <span class="font-mono font-bold ${b.dds.par >= 0 ? 'text-emerald-700' : 'text-rose-700'}">N/S ${b.dds.par > 0 ? '+' : ''}${b.dds.par}</span> <span class="text-slate-500 text-xs">${(b.dds.parc || []).map(resParContract).join(', ')}</span></div>` : '';
      return `<div class="mt-4"><p class="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2">${rt('dd')}</p>
        <table class="res-dd border-collapse"><tr><td class="border-0"></td>${cols.map(c => `<td class="border-0 text-base">${resStrainHtml(c)}</td>`).join('')}</tr>${rows}</table>${par}</div>`;
    }
    function resParContract(c) {
      // DDS dealer-par text, e.g. "4S-NS", "3H*-NS-1", "5C*-EW-2"
      const m = String(c).match(/^([1-7])([NSHDC])(\*?)-(NS|EW|N|S|E|W)(?:([+-]\d+))?$/);
      if (!m) return resEsc(c);
      return m[1] + resStrainHtml(m[2] === 'N' ? 'NT' : m[2]) + (m[3] ? 'X' : '') + ' ' + m[4] + (m[5] ? ' ' + m[5] : '');
    }
    function resSolverUrl(b) {
      const h = p => b.hands[p].join('.');
      const dn = (b.dealer || 'N').toLowerCase();
      const vn = { None: 'None', NS: 'NS', EW: 'EW', All: 'All' }[b.vul] || 'None';
      return `https://dds.bridgewebs.com/bsol2/ddummy.htm?club=jbf&board=${encodeURIComponent(b.bd)}&dealer=${dn}&vul=${vn}&north=${h('N')}&east=${h('E')}&south=${h('S')}&west=${h('W')}`;
    }
    function resHandDiagram(b, small) {
      if (!b.hands) return '';
      return `<div class="bg-white rounded-3xl border border-slate-200 p-4 ${small ? '' : 'sm:p-6 shadow-sm'}">
        <div class="flex items-center justify-between mb-3"><span class="font-black text-slate-900 ${small ? '' : 'text-lg'}">${rt('board')} ${resEsc(b.bd)}${b.sess && small ? ' <span class="text-xs text-slate-400">· ' + rt('session') + ' ' + resEsc(b.sess) + '</span>' : ''}</span>
          <span class="text-xs text-slate-500">${rt('dealer')} <b>${resEsc(b.dealer)}</b> · ${rt('vul')} <b>${resEsc(b.vul)}</b></span></div>
        <div class="res-hand ${small ? 'sm' : ''}"><div></div>${resSeat(b, 'N')}<div></div>${resSeat(b, 'W')}<div class="flex">${resCompass(b)}</div>${resSeat(b, 'E')}<div></div>${resSeat(b, 'S')}<div></div></div>
        ${resDDTable(b)}${b.commentary ? `<p class="mt-2 text-xs text-slate-600">${resEsc(b.commentary)}</p>` : ''}
        ${small ? '' : `<a href="${resSolverUrl(b)}" target="_blank" rel="noopener" class="res-noprint mt-4 inline-flex items-center gap-1.5 text-xs font-bold text-sky-700 hover:text-sky-900 bg-sky-50 px-3 py-2 rounded-xl"><i data-lucide="play-circle" class="w-4 h-4"></i>${rt('solver')}</a>`}</div>`;
    }

    // ---- board view: diagram + DD + leads + traveller ----
    function resGoBoard(i) { RES.board = i; RES.lead = null; if (RES.ev) resRenderEvent(); }
    const RES_COL = { NS: 'N/S', EW: 'E/W', Bid: 'contract', By: 'by', Ld: 'lead', Tks: 'tricks' };
    function resTravTable(s, b) {
      const pm = resPairMaps(s);
      const cols = b.cols || [];
      const iNS = cols.indexOf('NS'), iEW = cols.indexOf('EW');
      const cur = (resScorecardOptions(s).find(o => o.key === RES.pair)) || null;
      const head = cols.map((c, i) => {
        let l = RES_COL[c] ? (RES_T[RES_COL[c]] ? rt(RES_COL[c]) : RES_COL[c]) : c;
        if (c === '+Sc' || c === '-Sc') l = 'N/S ' + rt('score') + ' ' + (c === '+Sc' ? '+' : '−');
        if (i === cols.length - 2 && (c === '+' || c === 'NS X')) l = 'N/S ' + rt('points');
        if (i === cols.length - 1 && (c === '-' || c === 'EW X')) l = 'E/W ' + rt('points');
        return `<th>${resEsc(l)}</th>`;
      }).join('');
      const rows = b.rows.map(r => {
        const nmNS = pm.ns[r[iNS]] || '', nmEW = pm.ew[r[iEW]] || '';
        const sel = (cur && ((cur.dir !== 'EW' && r[iNS] === cur.no) || (cur.dir !== 'NS' && r[iEW] === cur.no))) || (RES.hl && resNorm(nmNS + ' ' + nmEW).includes(RES.hl));
        return `<tr class="${sel ? 'sel' : ''}">` + r.slice(0, cols.length).map((v, i) => {
          if (i === iNS || i === iEW) {
            const nm = i === iNS ? nmNS : nmEW;
            return `<td class="l"><span class="font-bold">${resEsc(v)}</span>${nm ? ' <span class="text-slate-500 text-xs">' + resEsc(nm) + '</span>' : ''}</td>`;
          }
          if (cols[i] === 'Bid') return `<td>${resContract(v)}</td>`;
          if (cols[i] === 'Ld') return `<td>${resCard(v)}</td>`;
          return `<td>${resEsc(v)}</td>`;
        }).join('') + '</tr>';
      }).join('');
      return `<div class="overflow-x-auto rounded-2xl border border-slate-200 shadow-xs"><table class="res-tbl"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div>`;
    }
    function resContractFreq(b) {
      const cols = b.cols || []; const ib = cols.indexOf('Bid'), iy = cols.indexOf('By');
      if (ib < 0) return '';
      const cnt = {};
      (b.rows || []).forEach(r => { const c = r[ib]; if (!c || c === '-' ) return; const k = c + (r[iy] ? ' ' + r[iy] : ''); cnt[k] = (cnt[k] || 0) + 1; });
      const list = Object.entries(cnt).sort((a, b) => b[1] - a[1]);
      if (!list.length) return '';
      return `<div class="mb-4"><p class="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2">${rt('freq')}</p><div class="flex flex-wrap gap-1.5">` +
        list.map(([k, n]) => { const [c, by] = k.split(' '); return `<span class="text-xs bg-slate-100 rounded-lg px-2 py-1">${resContract(c)} ${resEsc(by || '')} <b class="text-slate-500">${n}${rt('times')}</b></span>`; }).join('') + '</div></div>';
    }
    function resLeadsPanel(b) {
      if (!b.dds || !b.dds.leads) return '';
      // default contract: the most frequently played one, else the par contract
      if (!RES.lead) {
        let st = 'NT', decl = 'N';
        const cols = b.cols || []; const ib = cols.indexOf('Bid'), iy = cols.indexOf('By');
        const cnt = {};
        (b.rows || []).forEach(r => { const m = String(r[ib] || '').match(/^[1-7](NT|N|S|H|D|C)/); if (m && /^[NESW]$/.test(r[iy])) { const k = (m[1] === 'N' ? 'NT' : m[1]) + r[iy]; cnt[k] = (cnt[k] || 0) + 1; } });
        const best = Object.entries(cnt).sort((a, c) => c[1] - a[1])[0];
        if (best) { st = best[0].slice(0, -1); decl = best[0].slice(-1); }
        else if (b.dds.parc && b.dds.parc[0]) { const m = b.dds.parc[0].match(/^[1-7]([NSHDC])\*?-(NS|EW|N|E|S|W)/); if (m) { st = m[1] === 'N' ? 'NT' : m[1]; decl = m[2][0]; } }
        RES.lead = { st, decl };
      }
      const si = RES_STR.indexOf(RES.lead.st), di = 'NESW'.indexOf(RES.lead.decl);
      const leader = 'NESW'[(di + 1) % 4];
      const raw = (b.dds.leads[si] || [])[di] || '';
      const groups = {};
      raw.split(' ').filter(Boolean).forEach(x => { const [cards, t] = x.split(':'); (groups[t] = groups[t] || []).push(cards.match(/../g)); });
      const tricksSorted = Object.keys(groups).map(Number).sort((a, b) => a - b);
      const sel = `<div class="flex flex-wrap items-center gap-2 mb-3">
        <span class="text-xs font-bold text-slate-500">${rt('pickContract')}</span>
        ${RES_STR.map(s2 => `<button onclick="RES.lead.st='${s2}';resRenderEvent()" class="res-pill ${s2 === RES.lead.st ? 'on' : ''} w-10 h-8 rounded-lg text-sm font-bold bg-white border border-slate-300">${resStrainHtml(s2)}</button>`).join('')}
        <span class="text-xs font-bold text-slate-500 ml-2">${rt('declarer')}</span>
        ${'NESW'.split('').map(p => `<button onclick="RES.lead.decl='${p}';resRenderEvent()" class="res-pill ${p === RES.lead.decl ? 'on' : ''} w-8 h-8 rounded-lg text-sm font-bold bg-white border border-slate-300">${p}</button>`).join('')}</div>`;
      const body = tricksSorted.map((t, k) => `<div class="flex items-start gap-3 py-1.5 ${k ? 'border-t border-slate-100' : ''}">
          <span class="shrink-0 w-14 text-center rounded-lg px-2 py-1 text-sm font-black ${k === 0 ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600'}">${t}</span>
          <span class="flex flex-wrap gap-x-3 gap-y-1 text-base font-semibold">${groups[t].map(cs => cs.map(c => resCard(c[0] + c[1])).join('')).join('<span class="text-slate-300">·</span>')}</span></div>`).join('');
      return `<div class="mt-5 bg-slate-50 rounded-2xl border border-slate-200 p-4"><p class="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1">${rt('leads')}</p>
        <p class="text-xs text-slate-500 mb-3">${rt('leadHelp')} (${RES.lead.st === 'NT' ? 'NT' : RES_SUIT[RES.lead.st]} ${RES.lead.decl}, ${rt('lead')}: ${leader})</p>${sel}${body}</div>`;
    }
    function resRenderBoards(s) {
      const boards = s.boards || [];
      if (!boards.length) return resNoData();
      const i = Math.min(RES.board, boards.length - 1), b = boards[i];
      const bySess = {};
      boards.forEach((x, k) => { const key = x.sess || ''; (bySess[key] = bySess[key] || []).push(k); });
      const keys = Object.keys(bySess);
      const picker = '<div class="space-y-2 mb-5 res-noprint">' + keys.map(k =>
        `<div class="flex flex-wrap items-center gap-1.5">${keys.length > 1 ? `<span class="text-[10px] font-bold uppercase text-slate-400 mr-1 w-16">${rt('session')} ${resEsc(k)}</span>` : ''}` +
        bySess[k].map(j => `<button onclick="resGoBoard(${j})" class="res-pill ${j === i ? 'on' : ''} w-10 h-9 rounded-lg text-sm font-bold bg-white border border-slate-300 text-slate-700">${resEsc(boards[j].bd)}</button>`).join('') + '</div>').join('') + '</div>';
      const nav = `<div class="flex items-center justify-between mb-4 res-noprint">
          <button ${i > 0 ? `onclick="resGoBoard(${i - 1})"` : 'disabled'} class="inline-flex items-center gap-1 px-3 py-2 rounded-xl text-sm font-bold bg-white border border-slate-300 disabled:opacity-30"><i data-lucide="chevron-left" class="w-4 h-4"></i>${rt('prev')}</button>
          <span class="text-sm font-black text-slate-700">${rt('board')} ${resEsc(b.bd)} <span class="text-slate-400 font-normal">(${i + 1}/${boards.length})</span></span>
          <button ${i < boards.length - 1 ? `onclick="resGoBoard(${i + 1})"` : 'disabled'} class="inline-flex items-center gap-1 px-3 py-2 rounded-xl text-sm font-bold bg-white border border-slate-300 disabled:opacity-30">${rt('next')}<i data-lucide="chevron-right" class="w-4 h-4"></i></button></div>`;
      const trav = b.rows && b.rows.length;
      return picker + nav + `<div class="grid grid-cols-1 xl:grid-cols-5 gap-6">
          <div class="xl:col-span-2">${resHandDiagram(b) || `<p class="text-xs text-slate-500">${rt('board')} ${resEsc(b.bd)}</p>`}${resLeadsPanel(b)}</div>
          <div class="xl:col-span-3">${trav ? resContractFreq(b) + resTravTable(s, b) : ''}</div></div>
          ${b.dds ? `<p class="mt-6 text-[11px] text-slate-400">${rt('ddNote')}</p>` : ''}`;
    }
    function resRenderHands(s) {
      const hb = (s.boards || []).map((b, i) => [b, i]).filter(x => x[0].hands);
      if (!hb.length) return resNoData();
      const bySess = {};
      hb.forEach(x => { const k = x[0].sess || ''; (bySess[k] = bySess[k] || []).push(x); });
      const keys = Object.keys(bySess);
      return keys.map(k => (keys.length > 1 ? `<p class="text-xs font-bold uppercase tracking-wider text-sky-800 mb-3 mt-2">${rt('session')} ${resEsc(k)}</p>` : '') +
        `<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 mb-8">${bySess[k].map(([b, i]) => `<div class="cursor-pointer hover:-translate-y-0.5 transition-transform" onclick="resGoBoard(${i});RES.tab='travellers';resRenderEvent()">${resHandDiagram(b, true)}</div>`).join('')}</div>`).join('');
    }

    // ---- PBN export of the hand records ----
    function resDownloadPBN() {
      const ev = RES.ev, s = resSection();
      const vmap = { None: 'None', NS: 'NS', EW: 'EW', All: 'All' };
      const out = [];
      (s.boards || []).filter(b => b.hands).forEach(b => {
        out.push(`[Event "${ev.title.replace(/"/g, "'")}"]`, `[Site "Jordan Bridge Federation"]`, `[Date "${ev.date.replace(/-/g, '.')}"]`, `[Board "${b.bd}"]`,
          `[Dealer "${b.dealer}"]`, `[Vulnerable "${vmap[b.vul] || 'None'}"]`, `[Deal "N:${'NESW'.split('').map(p => b.hands[p].join('.')).join(' ')}"]`);
        if (b.dds) {
          const order = [0, 2, 1, 3]; // PBN: declarers N,S,E,W ; strains NT,S,H,D,C
          out.push(`[DoubleDummyTricks "${order.map(pi => RES_STR.map((st, si) => b.dds.t[si][pi].toString(16)).join('')).join('')}"]`);
          out.push(`[OptimumScore "NS ${b.dds.par}"]`);
        }
        out.push('');
      });
      const blob = new Blob([out.join('\r\n')], { type: 'text/plain' });
      const a = document.createElement('a'); a.href = URL.createObjectURL(blob);
      a.download = ev.id + (ev.sections.length > 1 ? '_s' + (RES.sec + 1) : '') + '.pbn'; a.click();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    }

    function resInitFromHash() {
      let m = location.hash.match(/^#results\/player\/(.+)$/);
      if (m) { document.getElementById('results').scrollIntoView(); resOpenPlayer(decodeURIComponent(m[1])); return; }
      m = location.hash.match(/^#results\/(\d{8}_\d+)(?:\/(\d+))?(?:\/(\w+))?(?:\/(.+))?$/);
      if (m) {
        document.getElementById('results').scrollIntoView();
        const o = { sec: m[2] ? +m[2] : 0, tab: m[3] || 'ranking' };
        if (o.tab === 'travellers' && m[4]) o.board = +m[4];
        if (o.tab === 'scorecards' && m[4]) o.pair = decodeURIComponent(m[4]);
        resOpenEvent(m[1], o);
      }
    }
'''
