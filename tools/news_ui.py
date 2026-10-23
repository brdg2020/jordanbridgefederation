# -*- coding: utf-8 -*-
"""Public "News & latest results" section, fed by the /admin panel (Firebase project jbf-portal).

The public page only reads published items through the Firestore REST API, so no
Firebase SDK is loaded for visitors. The section stays hidden while it is empty.
"""

NEWS_SECTION_HTML = r'''
  <!-- SECTION: NEWS & LATEST RESULTS (managed from /admin) -->
  <section id="news" class="py-14 bg-white border-b border-slate-200 hidden">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-2xl mx-auto mb-8">
        <span class="text-xs font-bold uppercase tracking-wider text-sky-800 bg-sky-100 px-3 py-1 rounded-full inline-block mb-2" data-en="Federation News" data-ar="أخبار الاتحاد">Federation News</span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="Announcements & Latest Results" data-ar="الإعلانات وأحدث النتائج">Announcements & Latest Results</h2>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div class="lg:col-span-3 space-y-4" id="newsAnnList"></div>
        <div class="lg:col-span-2 space-y-3" id="newsTourList"></div>
      </div>
    </div>
  </section>

  <div id="newsModal" class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm hidden items-start justify-center p-0 sm:p-4 overflow-y-auto" onclick="if(event.target===this) closeNewsTable()">
    <div class="bg-white w-full max-w-6xl sm:rounded-3xl shadow-2xl sm:my-4 overflow-hidden min-h-screen sm:min-h-0">
      <div class="bg-gradient-to-r from-sky-950 via-sky-900 to-slate-900 text-white px-5 sm:px-8 py-6 relative">
        <button onclick="closeNewsTable()" class="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20" aria-label="Close"><i data-lucide="x" class="w-5 h-5"></i></button>
        <p class="text-xs font-bold uppercase tracking-wider text-amber-300 pr-12" id="newsModalMeta"></p>
        <h3 class="text-xl sm:text-2xl font-black mt-1 pr-12" id="newsModalTitle"></h3>
        <p class="text-xs text-sky-100/80 mt-2" id="newsModalNote"></p>
      </div>
      <div class="px-3 sm:px-8 py-6" id="newsModalBody"></div>
    </div>
  </div>
'''

NEWS_JS = r'''
    // ===================== NEWS & LATEST RESULTS (from /admin, Firestore REST) =====================
    const NEWS = { ann: [], tour: [] };
    const FS_URL = 'https://firestore.googleapis.com/v1/projects/jbf-portal/databases/(default)/documents:runQuery?key=AIzaSyCQlYxWn-ARyz5caVrKtiOpBp-ahE65-xc';
    function fsVal(v) {
      if (!v) return null;
      if ('stringValue' in v) return v.stringValue;
      if ('booleanValue' in v) return v.booleanValue;
      if ('integerValue' in v) return +v.integerValue;
      if ('doubleValue' in v) return v.doubleValue;
      if ('timestampValue' in v) return v.timestampValue;
      return null;
    }
    async function fsPublished(col) {
      const body = { structuredQuery: { from: [{ collectionId: col }], where: { fieldFilter: { field: { fieldPath: 'published' }, op: 'EQUAL', value: { booleanValue: true } } }, limit: 200 } };
      const r = await fetch(FS_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      if (!r.ok) return [];
      const j = await r.json();
      return j.filter(x => x.document).map(x => { const o = { id: x.document.name.split('/').pop() }; Object.entries(x.document.fields || {}).forEach(([k, v]) => o[k] = fsVal(v)); return o; });
    }
    function newsEsc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
    function newsText(s) {
      // plain text with line breaks; web addresses become links
      return newsEsc(s).replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener nofollow" class="text-sky-700 underline break-all">$1</a>').replace(/\n/g, '<br>');
    }
    function newsDate(iso) { try { return new Date(iso + 'T12:00:00').toLocaleDateString(currentLang === 'ar' ? 'ar-JO' : 'en-GB', { day: 'numeric', month: 'long', year: 'numeric' }); } catch (e) { return iso; } }
    function renderNews() {
      const ar = currentLang === 'ar';
      const sec = document.getElementById('news');
      if (!NEWS.ann.length && !NEWS.tour.length) { sec.classList.add('hidden'); document.querySelectorAll('[data-sec=news]').forEach(a => a.classList.add('hidden')); return; }
      sec.classList.remove('hidden'); document.querySelectorAll('[data-sec=news]').forEach(a => a.classList.remove('hidden'));
      const anns = NEWS.ann.slice().sort((a, b) => (b.pinned - a.pinned) || (b.date || '').localeCompare(a.date || ''));
      document.getElementById('newsAnnList').innerHTML = anns.map(a => {
        const title = ar ? (a.title_ar || a.title_en) : (a.title_en || a.title_ar);
        const body = ar ? (a.body_ar || a.body_en) : (a.body_en || a.body_ar);
        const rtl = ar ? (a.title_ar || a.body_ar) : !(a.title_en || a.body_en);
        return `<article class="bg-slate-50 rounded-2xl border ${a.pinned ? 'border-amber-300' : 'border-slate-200'} p-5" ${rtl ? 'dir="rtl"' : ''}>
          <div class="flex items-center gap-2 text-xs text-slate-500 mb-1">${a.pinned ? '<span>📌</span>' : ''}<time>${newsEsc(newsDate(a.date))}</time></div>
          <h3 class="text-lg font-black text-slate-900">${newsEsc(title)}</h3>
          ${body ? `<p class="mt-2 text-sm text-slate-700 leading-relaxed">${newsText(body)}</p>` : ''}
          ${a.link ? `<a href="${newsEsc(a.link)}" target="_blank" rel="noopener nofollow" class="inline-block mt-3 text-sm font-bold text-sky-700 hover:underline">${ar ? 'المزيد' : 'Read more'} →</a>` : ''}
        </article>`;
      }).join('') || '';
      const tours = NEWS.tour.slice().sort((a, b) => (b.date || '').localeCompare(a.date || ''));
      document.getElementById('newsTourList').innerHTML = tours.length ? `<p class="text-xs font-bold uppercase tracking-wider text-slate-500">${ar ? 'أحدث النتائج' : 'Latest results'}</p>` + tours.map(t =>
        `<button onclick="openNewsTable('${t.id}')" class="w-full text-left bg-white rounded-2xl border border-slate-200 hover:border-sky-400 hover:shadow-md transition-all p-4">
          <div class="flex items-center justify-between gap-2 text-xs text-slate-500"><span>${newsEsc(newsDate(t.date))}</span><span class="font-bold text-sky-800">${newsEsc(t.category)}</span></div>
          <div class="font-extrabold text-slate-900 mt-1" ${ar && t.title_ar ? 'dir="rtl"' : ''}>${newsEsc(ar ? (t.title_ar || t.title) : t.title)}</div>
        </button>`).join('') : '';
    }
    function openNewsTable(id) {
      const t = NEWS.tour.find(x => x.id === id); if (!t) return;
      let tb = { header: [], rows: [] }; try { tb = JSON.parse(t.table); } catch (e) {}
      const ar = currentLang === 'ar';
      document.getElementById('newsModalMeta').textContent = newsDate(t.date) + ' · ' + (t.category || '');
      document.getElementById('newsModalTitle').textContent = ar ? (t.title_ar || t.title) : t.title;
      document.getElementById('newsModalNote').textContent = t.note || '';
      const top = v => /^[123]=?$/.test(v) ? `<span class="badge-rank-${v[0]} inline-flex items-center justify-center min-w-7 h-7 px-1.5 rounded-full text-xs font-black">${newsEsc(v)}</span>` : newsEsc(v);
      document.getElementById('newsModalBody').innerHTML = `<div class="overflow-x-auto rounded-2xl border border-slate-200"><table class="res-tbl">
        <thead><tr>${tb.header.map(h => `<th>${newsEsc(h)}</th>`).join('')}</tr></thead>
        <tbody>${tb.rows.map(r => `<tr>${r.map((c, i) => `<td class="${String(c).length > 18 ? 'l' : ''}">${i === 0 ? top(c) : newsEsc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
      const m = document.getElementById('newsModal'); m.classList.remove('hidden'); m.classList.add('flex'); document.body.style.overflow = 'hidden';
      lucide.createIcons();
    }
    function closeNewsTable() { const m = document.getElementById('newsModal'); m.classList.add('hidden'); m.classList.remove('flex'); document.body.style.overflow = ''; }
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNewsTable(); });
    async function loadNews() {
      try {
        const [a, t] = await Promise.all([fsPublished('announcements'), fsPublished('tournaments')]);
        NEWS.ann = a; NEWS.tour = t; renderNews();
      } catch (e) { /* the rest of the site works without this section */ }
    }
'''
