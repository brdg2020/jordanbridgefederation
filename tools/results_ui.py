# -*- coding: utf-8 -*-
"""HTML + JS for the "Results" section (Bridgewebs archive), injected by build_site.py.

Kept as plain (non f-string) text so the JavaScript needs no brace escaping.
Data: public/data/results/index.json (embedded at build time) and
public/data/results/events/<id>.json (fetched when an event is opened).
"""

RESULTS_SECTION_HTML = r'''
  <!-- SECTION: RESULTS ARCHIVE (migrated from bridgewebs.com/jbf) -->
  <section id="results" class="py-16 bg-slate-100 border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

      <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-sky-600"></span>
            <span class="text-xs font-bold uppercase tracking-wider text-sky-800" data-en="Results Archive" data-ar="أرشيف النتائج">Results Archive</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-1" data-en="Tournament Results 2019 – 2026" data-ar="نتائج البطولات 2019 – 2026">Tournament Results 2019 – 2026</h2>
          <p class="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl" data-en="Every event published on the federation's Bridgewebs results calendar: rankings, match results, scorecards, travellers and hand records. Click an event to open it." data-ar="جميع البطولات المنشورة في تقويم نتائج الاتحاد على Bridgewebs: الترتيب ونتائج المباريات وبطاقات النتائج وجداول اللوحات وتوزيعات الأوراق. اضغط على أي بطولة لعرض التفاصيل.">Every event published on the federation's Bridgewebs results calendar: rankings, match results, scorecards, travellers and hand records. Click an event to open it.</p>
        </div>
        <div class="relative w-full md:w-72">
          <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-3"></i>
          <input type="text" id="resSearchInput" oninput="resSetSearch(this.value)" placeholder="Search events..." class="w-full pl-10 pr-4 py-2 text-sm bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 shadow-xs">
        </div>
      </div>

      <div class="flex flex-col gap-3 mb-6">
        <div class="flex flex-wrap items-center gap-2 bg-white p-1.5 rounded-2xl border border-slate-300 shadow-xs w-fit max-w-full" id="resYearBar"></div>
        <div class="flex flex-wrap items-center gap-2" id="resCatBar"></div>
      </div>

      <p class="text-xs text-slate-500 mb-4" id="resCountLine"></p>
      <div id="resListContainer" class="space-y-10"></div>
    </div>
  </section>

  <!-- RESULTS EVENT DETAIL MODAL -->
  <div id="resModal" class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm hidden items-start justify-center p-2 sm:p-6 overflow-y-auto" onclick="if(event.target===this) resCloseEvent()">
    <div class="bg-white w-full max-w-6xl rounded-3xl shadow-2xl border border-slate-200 my-4 overflow-hidden">
      <div class="bg-gradient-to-r from-sky-950 via-sky-900 to-slate-900 text-white px-5 sm:px-8 py-6 relative">
        <button onclick="resCloseEvent()" class="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20" aria-label="Close"><i data-lucide="x" class="w-5 h-5"></i></button>
        <p class="text-xs font-bold uppercase tracking-wider text-amber-300" id="resModalMeta"></p>
        <h3 class="text-xl sm:text-2xl font-black mt-1 pr-10" id="resModalTitle"></h3>
        <p class="text-xs text-sky-100/80 mt-2" id="resModalStaff"></p>
      </div>
      <div class="px-4 sm:px-8 pt-5">
        <div class="flex flex-wrap gap-2 mb-3" id="resSectionBar"></div>
        <div class="inline-flex flex-wrap p-1 bg-slate-100 border border-slate-200 rounded-2xl gap-1" id="resTabBar"></div>
      </div>
      <div class="px-4 sm:px-8 py-6" id="resModalBody"></div>
      <div class="px-4 sm:px-8 pb-6 text-[11px] text-slate-400" id="resModalSource"></div>
    </div>
  </div>
'''

RESULTS_CSS = r'''
    .res-pill { transition: all .15s; }
    .res-pill.on { background:#0369a1; color:#fff; border-color:#0369a1; box-shadow:0 1px 2px rgba(0,0,0,.08); }
    .res-tbl { border-collapse: collapse; width: 100%; font-size: 13px; }
    .res-tbl th, .res-tbl td.h { background:#0f172a; color:#fff; font-weight:700; font-size:11px; text-transform:uppercase; letter-spacing:.03em; padding:8px 10px; text-align:center; white-space:nowrap; border:1px solid #1e293b; }
    .res-tbl td { padding:6px 10px; border-bottom:1px solid #e2e8f0; text-align:center; white-space:nowrap; }
    .res-tbl td.l { text-align:left; white-space:normal; min-width:160px; }
    .res-tbl tbody tr:nth-child(even) td:not(.h) { background:#f8fafc; }
    .res-tbl tbody tr:hover td:not(.h) { background:#e0f2fe; }
    .res-tbl tr.sel td { background:#fef3c7 !important; }
    .suit-s, .suit-c { color:#0f172a; } .suit-h, .suit-d { color:#dc2626; }
    .res-hand { display:grid; grid-template-columns: 1fr 1fr 1fr; grid-template-rows:auto auto auto; gap:6px; font-size:13px; line-height:1.35; }
    .res-hand .seat { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; white-space:nowrap; }
    .res-hand .ctr { display:flex; align-items:center; justify-content:center; }
    .res-compass { width:86px; height:86px; border-radius:14px; background:#0f172a; color:#fff; position:relative; font-weight:800; font-size:11px; }
    .res-compass span { position:absolute; padding:1px 5px; border-radius:6px; }
    .res-compass .vul { background:#dc2626; } .res-compass .nv { background:#16a34a; }
    .res-compass .n { top:4px; left:50%; transform:translateX(-50%); } .res-compass .s { bottom:4px; left:50%; transform:translateX(-50%); }
    .res-compass .w { left:4px; top:50%; transform:translateY(-50%); } .res-compass .e { right:4px; top:50%; transform:translateY(-50%); }
    .res-compass .bd { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-size:20px; }
    .res-compass .dl { text-decoration: underline; text-underline-offset: 2px; }
'''

RESULTS_JS = r'''
    // ===================== RESULTS ARCHIVE (Bridgewebs migration) =====================
    const RES = { index: resultsIndex, year: 'all', cat: 'all', q: '', cache: {}, ev: null, sec: 0, tab: 'ranking', board: 0, pair: '', team: 0 };
    const RES_CATS = ['Jordan Bridge Festival', "Jordan Cup", 'Selection & Qualification', 'Other Events'];
    const RES_T = {
      all: ['All', 'الكل'], allYears: ['All years', 'كل السنوات'], events: ['events', 'بطولة'],
      ranking: ['Ranking', 'الترتيب'], matches: ['Matches', 'المباريات'], scorecards: ['Scorecards', 'بطاقات النتائج'],
      travellers: ['Travellers', 'جداول اللوحات'], hands: ['Hands', 'توزيع الأوراق'], ximps: ['X-Imps', 'X-Imps'],
      information: ['Information', 'معلومات'], board: ['Board', 'لوحة'], pair: ['Pair / Team', 'الزوج / الفريق'],
      loading: ['Loading…', 'جارٍ التحميل…'], noData: ['Bridgewebs has no data of this kind for this event.', 'لا تتوفر بيانات من هذا النوع لهذه البطولة على Bridgewebs.'],
      source: ['Source: Bridgewebs results page', 'المصدر: صفحة النتائج على Bridgewebs'], tables: ['tables', 'طاولات'],
      dealer: ['Dealer', 'الموزع'], vul: ['Vul', 'الخطورة'], hcp: ['HCP', 'النقاط'], dd: ['Makeable contracts (double dummy)', 'العقود الممكنة (Double Dummy)'],
      session: ['Session', 'الجلسة'], selectPair: ['Select a pair or team', 'اختر زوجًا أو فريقًا'], vs: ['Opponents', 'الخصوم'],
      dir: ['Dir', 'الاتجاه'], contract: ['Contract', 'العقد'], by: ['By', 'المنفذ'], lead: ['Lead', 'الافتتاح'], tricks: ['Tricks', 'اللمّات'],
      score: ['Score', 'النتيجة'], points: ['Points', 'النقاط'], names: ['Show names', 'إظهار الأسماء'], loadErr: ['Could not load this event. Please try again.', 'تعذر تحميل البطولة. حاول مرة أخرى.'],
      type_Pairs: ['Pairs', 'أزواج'], 'type_Butler Pairs': ['Butler Pairs', 'أزواج (Butler)'], type_Teams: ['Teams', 'فرق'],
      'cat_Jordan Bridge Festival': ['Jordan Bridge Festival', 'مهرجان الأردن للبريدج'], 'cat_Jordan Cup': ["Jordan Cup", 'كأس الأردن'],
      'cat_Selection & Qualification': ['Selection & Qualification', 'التصفيات والاختيار'], 'cat_Other Events': ['Other Events', 'بطولات أخرى']
    };
    function rt(k) { const v = RES_T[k]; return v ? v[currentLang === 'ar' ? 1 : 0] : k; }
    function resEsc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
    function resDate(iso) {
      const d = new Date(iso + 'T12:00:00');
      return d.toLocaleDateString(currentLang === 'ar' ? 'ar-JO' : 'en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
    }
    const RES_SUIT = { S: '<span class="suit-s">♠</span>', H: '<span class="suit-h">♥</span>', D: '<span class="suit-d">♦</span>', C: '<span class="suit-c">♣</span>' };
    function resSuitText(s) {
      // turns suit symbols already in text into coloured spans
      return resEsc(s).replace(/♠/g, RES_SUIT.S).replace(/♥/g, RES_SUIT.H).replace(/♦/g, RES_SUIT.D).replace(/♣/g, RES_SUIT.C);
    }
    function resContract(c) {
      if (!c) return '';
      const m = String(c).match(/^([1-7])(NT|N|S|H|D|C)(\*{0,2})(.*)$/);
      if (!m) return resEsc(c);
      const st = m[2] === 'NT' || m[2] === 'N' ? 'NT' : RES_SUIT[m[2]];
      const dbl = m[3] === '**' ? 'XX' : (m[3] === '*' ? 'X' : '');
      return m[1] + st + dbl + resEsc(m[4]);
    }
    function resCard(c) {
      if (!c) return '';
      const m = String(c).match(/^([SHDC])(.+)$/);
      return m ? RES_SUIT[m[1]] + resEsc(m[2] === 'T' ? '10' : m[2]) : resEsc(c);
    }

    // ---------- list ----------
    function resSetSearch(v) { RES.q = v.trim().toLowerCase(); renderResultsList(); }
    function resSetYear(y) { RES.year = y; renderResultsList(); }
    function resSetCat(c) { RES.cat = c; renderResultsList(); }

    function renderResultsList() {
      const evs = RES.index.events;
      const years = [...new Set(evs.map(e => e.year))].sort((a, b) => b - a);
      const pill = (on, label, fn) => `<button onclick="${fn}" class="res-pill ${on ? 'on' : ''} px-3.5 py-1.5 rounded-xl text-xs font-bold border border-transparent text-slate-700 hover:bg-slate-100">${label}</button>`;
      document.getElementById('resYearBar').innerHTML = pill(RES.year === 'all', rt('allYears'), "resSetYear('all')") +
        years.map(y => pill(RES.year == y, y, `resSetYear(${y})`)).join('');
      const chip = (on, label, n, fn) => `<button onclick="${fn}" class="res-pill ${on ? 'on' : ''} px-3 py-1.5 rounded-full text-xs font-bold bg-white border border-slate-300 text-slate-700 hover:bg-slate-50">${label} <span class="opacity-60">${n}</span></button>`;
      const inYear = evs.filter(e => RES.year === 'all' || e.year == RES.year);
      document.getElementById('resCatBar').innerHTML = chip(RES.cat === 'all', rt('all'), inYear.length, "resSetCat('all')") +
        RES_CATS.filter(c => inYear.some(e => e.category === c)).map(c => chip(RES.cat === c, rt('cat_' + c), inYear.filter(e => e.category === c).length, `resSetCat('${c.replace(/'/g, "\\'")}')`)).join('');

      const list = inYear.filter(e => (RES.cat === 'all' || e.category === RES.cat) &&
        (!RES.q || (e.title + ' ' + e.date + ' ' + e.type + ' ' + e.category + ' ' + (e.staff || []).join(' ')).toLowerCase().includes(RES.q)));
      document.getElementById('resCountLine').textContent = list.length + ' ' + rt('events');
      const out = [];
      years.forEach(y => {
        const ye = list.filter(e => e.year === y);
        if (!ye.length) return;
        out.push(`<div><div class="flex items-center gap-3 mb-4"><h3 class="text-2xl font-black text-slate-900">${y}</h3><span class="h-px flex-1 bg-slate-300"></span><span class="text-xs font-bold text-slate-500">${ye.length} ${rt('events')}</span></div>`);
        RES_CATS.forEach(c => {
          const ce = ye.filter(e => e.category === c);
          if (!ce.length) return;
          out.push(`<p class="text-xs font-bold uppercase tracking-wider text-sky-800 mb-2 mt-4">${rt('cat_' + c)}</p><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">`);
          ce.forEach(e => {
            const tags = [];
            if (e.travellers) tags.push(rt('travellers'));
            if (e.hands) tags.push(rt('hands'));
            if (e.matches) tags.push(rt('matches'));
            out.push(`<button onclick="resOpenEvent('${e.id}')" class="text-left bg-white rounded-2xl border border-slate-200 hover:border-sky-400 hover:shadow-md transition-all p-4 flex flex-col gap-2 group">
              <div class="flex items-center justify-between gap-2">
                <span class="text-[11px] font-bold text-slate-500">${resDate(e.date)}</span>
                <span class="text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full ${e.type === 'Teams' ? 'bg-emerald-100 text-emerald-800' : (e.type === 'Butler Pairs' ? 'bg-amber-100 text-amber-800' : 'bg-sky-100 text-sky-800')}">${rt('type_' + e.type)}</span>
              </div>
              <span class="font-extrabold text-slate-900 leading-snug group-hover:text-sky-800">${resEsc(e.title)}</span>
              <span class="text-[11px] text-slate-500">${e.tables ? resEsc(e.tables) + ' ' + rt('tables') : ''}${e.tables && e.staff.length ? ' · ' : ''}${resEsc((e.staff || []).join(' · '))}</span>
              <span class="flex flex-wrap gap-1 mt-1">${[rt('ranking')].concat(tags).map(t => `<span class="text-[10px] font-semibold px-1.5 py-0.5 rounded-md bg-slate-100 text-slate-600">${t}</span>`).join('')}</span>
            </button>`);
          });
          out.push('</div>');
        });
        out.push('</div>');
      });
      document.getElementById('resListContainer').innerHTML = out.join('') || `<p class="text-sm text-slate-500">–</p>`;
    }

    // ---------- detail ----------
    async function resOpenEvent(id, keepState) {
      const meta = RES.index.events.find(e => e.id === id);
      if (!meta) return;
      const modal = document.getElementById('resModal');
      modal.classList.remove('hidden'); modal.classList.add('flex');
      document.body.style.overflow = 'hidden';
      document.getElementById('resModalMeta').textContent = resDate(meta.date) + ' · ' + rt('cat_' + meta.category) + ' · ' + rt('type_' + meta.type);
      document.getElementById('resModalTitle').textContent = meta.title;
      document.getElementById('resModalStaff').textContent = [meta.tables ? meta.tables + ' ' + rt('tables') : ''].concat(meta.staff || []).filter(Boolean).join(' · ');
      if (!keepState) { RES.sec = 0; RES.tab = 'ranking'; RES.board = 0; RES.pair = ''; RES.team = 0; }
      if (location.hash !== '#results/' + id) history.replaceState(null, '', '#results/' + id);
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
      lucide.createIcons();
    }
    function resCloseEvent() {
      const modal = document.getElementById('resModal');
      modal.classList.add('hidden'); modal.classList.remove('flex');
      document.body.style.overflow = '';
      RES.ev = null;
      if (location.hash.startsWith('#results/')) history.replaceState(null, '', '#results');
    }
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && RES.ev) resCloseEvent(); });

    function resSection() { return RES.ev.sections[RES.sec] || RES.ev.sections[0]; }
    function resTabsFor(s) {
      const t = ['ranking'];
      if (s.matches && s.matches.length) t.push('matches');
      const trav = (s.boards || []).some(b => b.rows && b.rows.length);
      if (trav && s.pairs && s.pairs.length) t.push('scorecards');
      if (trav) t.push('travellers');
      if ((s.boards || []).some(b => b.hands)) t.push('hands');
      if (s.ximps && s.ximps.length) t.push('ximps');
      if (s.information) t.push('information');
      return t;
    }
    function resSetSec(i) { RES.sec = i; RES.board = 0; RES.pair = ''; RES.team = 0; const t = resTabsFor(resSection()); if (!t.includes(RES.tab)) RES.tab = 'ranking'; resRenderEvent(); }
    function resSetTab(t) { RES.tab = t; resRenderEvent(); }

    function resRenderEvent() {
      const ev = RES.ev, s = resSection();
      document.getElementById('resSectionBar').innerHTML = ev.sections.length > 1 ? ev.sections.map((x, i) =>
        `<button onclick="resSetSec(${i})" class="res-pill ${i === RES.sec ? 'on' : ''} px-3 py-1.5 rounded-full text-xs font-bold bg-white border border-slate-300 text-slate-700">${resEsc(x.label || (rt('session') + ' ' + (i + 1)))}</button>`).join('') : '';
      const tabs = resTabsFor(s);
      if (!tabs.includes(RES.tab)) RES.tab = 'ranking';
      document.getElementById('resTabBar').innerHTML = tabs.map(t =>
        `<button onclick="resSetTab('${t}')" class="res-pill ${t === RES.tab ? 'on' : ''} px-4 py-2 rounded-xl text-xs sm:text-sm font-bold text-slate-700 hover:bg-white">${rt(t)}</button>`).join('');
      const body = document.getElementById('resModalBody');
      const fn = { ranking: resRenderRanking, matches: resRenderMatches, scorecards: resRenderScorecards, travellers: resRenderTravellers, hands: resRenderHands, ximps: resRenderXimps, information: resRenderInfo }[RES.tab];
      body.innerHTML = fn(s);
    }

    // generic Bridgewebs table (cells: {t, cs, rs, h})
    function resGenericTable(rows, opts) {
      opts = opts || {};
      const html = ['<div class="overflow-x-auto rounded-2xl border border-slate-200"><table class="res-tbl"><tbody>'];
      rows.forEach(r => {
        html.push('<tr>');
        r.forEach((c, ci) => {
          const attrs = (c.cs ? ` colspan="${c.cs}"` : '') + (c.rs ? ` rowspan="${c.rs}"` : '');
          let txt = c.t || '';
          let inner = resSuitText(txt).replace(/\n/g, '<br>');
          if (!c.h && opts.rankCol === ci && /^[123]=?$/.test(txt)) {
            inner = `<span class="badge-rank-${txt[0]} inline-flex items-center justify-center min-w-7 h-7 px-1.5 rounded-full text-xs font-black">${resEsc(txt)}</span>`;
          }
          const cls = c.h ? 'h' : (txt.length > 18 || txt.includes('\n') ? 'l' : '');
          html.push(`<td class="${cls}"${attrs}>${inner}</td>`);
        });
        html.push('</tr>');
      });
      html.push('</tbody></table></div>');
      return html.join('');
    }
    function resNoData() { return `<p class="text-sm text-slate-500">${rt('noData')}</p>`; }

    function resRenderRanking(s) {
      const rk = s.ranking || {};
      const parts = (rk.tables || []).map(t => resGenericTable(t, { rankCol: 0 }));
      if (rk.info && rk.info.length) {
        parts.push('<dl class="mt-5 grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-1 text-xs text-slate-600">' +
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

    // ---- pair names ----
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

    // ---- hand diagram ----
    function resSuitLine(suit, cards) {
      const c = cards ? cards.replace(/T/g, '10') : '—';
      return `<div>${RES_SUIT[suit]} ${resEsc(c)}</div>`;
    }
    function resSeat(b, seat) {
      const h = b.hands[seat];
      return `<div class="seat"><div class="text-[10px] font-bold text-slate-400 uppercase">${seat}${b.hcp && b.hcp[seat] ? ' · ' + resEsc(b.hcp[seat]) : ''}</div>` +
        ['S', 'H', 'D', 'C'].map((st, i) => resSuitLine(st, h[i])).join('') + '</div>';
    }
    function resCompass(b) {
      const nsV = b.vul === 'NS' || b.vul === 'All', ewV = b.vul === 'EW' || b.vul === 'All';
      const sp = (k, v) => `<span class="${k} ${v ? 'vul' : 'nv'} ${b.dealer === k.toUpperCase() ? 'dl' : ''}">${k.toUpperCase()}</span>`;
      return `<div class="res-compass">${sp('n', nsV)}${sp('s', nsV)}${sp('w', ewV)}${sp('e', ewV)}<div class="bd">${resEsc(b.bd)}</div></div>`;
    }
    function resDDTable(b) {
      let lv = null;
      if (b.dd) {
        lv = {};
        Object.keys(b.dd).forEach(p => { lv[p] = {}; Object.keys(b.dd[p]).forEach(st => { const t = parseInt(b.dd[p][st], 10); lv[p][st] = isNaN(t) ? '' : (t > 6 ? String(t - 6) : '-'); }); });
      } else if (b.ddl) lv = b.ddl;
      if (!lv) return '';
      const cols = ['C', 'D', 'H', 'S', 'NT'];
      return `<div class="mt-3"><p class="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">${rt('dd')}</p><table class="text-xs border-collapse"><tr><td></td>${cols.map(c => `<td class="px-2 text-center font-bold">${c === 'NT' ? 'NT' : RES_SUIT[c]}</td>`).join('')}</tr>` +
        ['N', 'S', 'E', 'W'].filter(p => lv[p]).map(p => `<tr><td class="pr-2 font-bold text-slate-500">${p}</td>${cols.map(c => `<td class="px-2 text-center border border-slate-200">${resEsc(lv[p][c] || '')}</td>`).join('')}</tr>`).join('') + '</table></div>';
    }
    function resHandDiagram(b, compact) {
      if (!b.hands) return '';
      return `<div class="bg-white rounded-2xl border border-slate-200 p-3 ${compact ? '' : 'sm:p-4'}">
        <div class="flex items-center justify-between mb-2"><span class="font-black text-slate-900">${rt('board')} ${resEsc(b.bd)}</span><span class="text-[11px] text-slate-500">${rt('dealer')}: ${resEsc(b.dealer)} · ${rt('vul')}: ${resEsc(b.vul)}</span></div>
        <div class="res-hand"><div></div>${resSeat(b, 'N')}<div></div>${resSeat(b, 'W')}<div class="ctr">${resCompass(b)}</div>${resSeat(b, 'E')}<div></div>${resSeat(b, 'S')}<div></div></div>
        ${resDDTable(b)}${b.commentary ? `<p class="mt-2 text-xs text-slate-600">${resEsc(b.commentary)}</p>` : ''}</div>`;
    }

    // ---- board navigation (grouped by session) ----
    function resBoardPicker(boards, onclickFn) {
      const bySess = {};
      boards.forEach((b, i) => { const k = b.sess || ''; (bySess[k] = bySess[k] || []).push(i); });
      const keys = Object.keys(bySess);
      return '<div class="space-y-2 mb-5">' + keys.map(k =>
        `<div class="flex flex-wrap items-center gap-1.5">${keys.length > 1 ? `<span class="text-[10px] font-bold uppercase text-slate-400 mr-1 w-16">${rt('session')} ${resEsc(k)}</span>` : ''}` +
        bySess[k].map(i => `<button onclick="${onclickFn}(${i})" class="res-pill ${i === RES.board ? 'on' : ''} w-9 h-8 rounded-lg text-xs font-bold bg-white border border-slate-300 text-slate-700">${resEsc(boards[i].bd)}</button>`).join('') + '</div>').join('') + '</div>';
    }
    function resGoBoard(i) { RES.board = i; resRenderEvent(); }

    const RES_COL = { NS: 'N/S', EW: 'E/W', Bid: 'contract', By: 'by', Ld: 'lead', Tks: 'tricks', '+Sc': '+', '-Sc': '−' };
    function resTravTable(s, b, hiPair) {
      const pm = resPairMaps(s);
      const cols = b.cols || [];
      const iNS = cols.indexOf('NS'), iEW = cols.indexOf('EW');
      const head = cols.map((c, i) => {
        let l = RES_COL[c] ? (RES_T[RES_COL[c]] ? rt(RES_COL[c]) : RES_COL[c]) : c;
        if (c === '+Sc' || c === '-Sc') l = rt('score') + ' ' + (c === '+Sc' ? '+' : '−');
        if (i === cols.length - 2 && (c === '+' || c === 'NS X')) l = 'N/S ' + rt('points');
        if (i === cols.length - 1 && (c === '-' || c === 'EW X')) l = 'E/W ' + rt('points');
        return `<th>${resEsc(l)}</th>`;
      }).join('');
      const rows = b.rows.map(r => {
        const sel = hiPair && ((hiPair.dir !== 'EW' && r[iNS] === hiPair.no) || (hiPair.dir !== 'NS' && r[iEW] === hiPair.no));
        return `<tr class="${sel ? 'sel' : ''}">` + r.slice(0, cols.length).map((v, i) => {
          if (i === iNS || i === iEW) {
            const nm = (i === iNS ? pm.ns : pm.ew)[v];
            return `<td class="l"><span class="font-bold">${resEsc(v)}</span>${nm ? ' <span class="text-slate-500 text-xs">' + resEsc(nm) + '</span>' : ''}</td>`;
          }
          if (cols[i] === 'Bid') return `<td>${resContract(v)}</td>`;
          if (cols[i] === 'Ld') return `<td>${resCard(v)}</td>`;
          return `<td>${resEsc(v)}</td>`;
        }).join('') + '</tr>';
      }).join('');
      return `<div class="overflow-x-auto rounded-2xl border border-slate-200"><table class="res-tbl"><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div>`;
    }

    function resRenderTravellers(s) {
      const boards = s.boards || [];
      if (!boards.length) return resNoData();
      const i = Math.min(RES.board, boards.length - 1), b = boards[i];
      return resBoardPicker(boards, 'resGoBoard') +
        `<div class="grid grid-cols-1 lg:grid-cols-3 gap-5"><div>${resHandDiagram(b) || `<p class="text-xs text-slate-500">${rt('board')} ${resEsc(b.bd)}</p>`}</div>
         <div class="lg:col-span-2">${b.rows && b.rows.length ? resTravTable(s, b) : resNoData()}</div></div>`;
    }
    function resRenderHands(s) {
      const hb = (s.boards || []).filter(b => b.hands);
      if (!hb.length) return resNoData();
      const bySess = {};
      hb.forEach(b => { const k = b.sess || ''; (bySess[k] = bySess[k] || []).push(b); });
      const keys = Object.keys(bySess);
      return keys.map(k => (keys.length > 1 ? `<p class="text-xs font-bold uppercase tracking-wider text-sky-800 mb-2 mt-2">${rt('session')} ${resEsc(k)}</p>` : '') +
        `<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">${bySess[k].map(b => resHandDiagram(b, true)).join('')}</div>`).join('');
    }

    // ---- scorecards: each pair's line taken from the travellers ----
    function resScorecardOptions(s) {
      const pm = resPairMaps(s);
      const opts = [];
      // only pairs/teams that appear on at least one traveller (skips byes / non-playing entries)
      const seenNS = new Set(), seenEW = new Set();
      (s.boards || []).forEach(b => { const c = b.cols || [], i = c.indexOf('NS'), j = c.indexOf('EW'); (b.rows || []).forEach(r => { seenNS.add(r[i]); seenEW.add(r[j]); }); });
      (s.pairs || []).forEach(p => {
        const dir = pm.mitchell ? (p.way === '2' ? 'EW' : 'NS') : '';
        if (dir === 'NS' ? !seenNS.has(p.pair) : dir === 'EW' ? !seenEW.has(p.pair) : !(seenNS.has(p.pair) || seenEW.has(p.pair))) return;
        opts.push({ key: dir + ':' + p.pair, no: p.pair, dir, label: (dir ? dir + ' ' : '') + p.pair + ' — ' + p.names.filter(Boolean).join(' & ') });
      });
      return opts;
    }
    function resRenderScorecards(s) {
      const opts = resScorecardOptions(s);
      if (!opts.length) return resNoData();
      if (!RES.pair) RES.pair = opts[0].key;
      const cur = opts.find(o => o.key === RES.pair) || opts[0];
      const pm = resPairMaps(s);
      const sel = `<div class="mb-4 flex flex-wrap items-center gap-3"><label class="text-xs font-bold text-slate-500">${rt('pair')}</label>
        <select onchange="RES.pair=this.value;resRenderEvent()" class="text-sm p-2 border border-slate-300 rounded-xl bg-white max-w-full">${opts.map(o => `<option value="${resEsc(o.key)}" ${o.key === cur.key ? 'selected' : ''}>${resEsc(o.label)}</option>`).join('')}</select></div>`;
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
          const oppName = (dir === 'NS' ? pm.ew : pm.ns)[opp] || '';
          const plus = g('+Sc'), minus = g('-Sc');
          // score shown from this pair's side: Bridgewebs lists N/S + and N/S − columns
          let sc = '';
          if (dir === 'NS') sc = plus && plus !== '-' ? plus : (minus && minus !== '-' ? '−' + minus : (plus || minus));
          else sc = minus && minus !== '-' ? minus : (plus && plus !== '-' ? '−' + plus : (plus || minus));
          const pts = dir === 'NS' ? r[cols.length - 2] : r[cols.length - 1];
          lines.push(`<tr><td><button class="font-bold text-sky-700 underline" onclick="RES.board=${bi};RES.tab='travellers';resRenderEvent()">${resEsc(b.bd)}</button></td>${b.sess && s.boards.some(x => x.sess !== b.sess) ? `<td>${resEsc(b.sess)}</td>` : ''}<td>${dir === 'NS' ? 'N/S' : 'E/W'}</td>
            <td class="l"><span class="font-bold">${resEsc(opp)}</span> <span class="text-xs text-slate-500">${resEsc(oppName)}</span></td>
            <td>${resContract(g('Bid'))}</td><td>${resEsc(g('By'))}</td>${cols.includes('Ld') ? `<td>${resCard(g('Ld'))}</td>` : ''}<td>${resEsc(g('Tks'))}</td><td>${resEsc(sc)}</td><td class="font-bold">${resEsc(pts)}</td></tr>`);
        });
      });
      const multiSess = (s.boards || []).some(x => x.sess !== (s.boards[0] || {}).sess);
      const hasLd = (s.boards || []).some(b => (b.cols || []).includes('Ld'));
      const head = `<tr><th>${rt('board')}</th>${multiSess ? `<th>${rt('session')}</th>` : ''}<th>${rt('dir')}</th><th>${rt('vs')}</th><th>${rt('contract')}</th><th>${rt('by')}</th>${hasLd ? `<th>${rt('lead')}</th>` : ''}<th>${rt('tricks')}</th><th>${rt('score')}</th><th>${rt('points')}</th></tr>`;
      return sel + (lines.length ? `<div class="overflow-x-auto rounded-2xl border border-slate-200"><table class="res-tbl"><thead>${head}</thead><tbody>${lines.join('')}</tbody></table></div>` : resNoData());
    }

    function resInitFromHash() {
      const m = location.hash.match(/^#results\/(\d{8}_\d+)$/);
      if (m) { document.getElementById('results').scrollIntoView(); resOpenEvent(m[1]); }
    }
'''
