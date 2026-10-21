import os

base_dir = os.path.dirname(os.path.abspath(__file__))
build_site_path = os.path.join(base_dir, 'build_site.py')

with open(build_site_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = """    // Render Jordan Cup Cards
    function renderJordanCup() {{
      const container = document.getElementById('jordanCupCards');
      container.innerHTML = '';

      jordanCupData.teams.forEach(t => {{
        const card = document.createElement('div');
        card.className = 'bg-white p-5 rounded-2xl border border-slate-200 hover:border-emerald-400 hover:shadow-xs transition-all flex flex-col justify-between';
        
        let rankColor = 'bg-slate-200 text-slate-800';
        if (t.rank === 1) rankColor = 'bg-amber-400 text-slate-950 font-black';
        else if (t.rank === 2) rankColor = 'bg-slate-300 text-slate-900 font-black';
        else if (t.rank === 3) rankColor = 'bg-orange-300 text-orange-950 font-black';

        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="w-8 h-8 rounded-xl flex items-center justify-center text-xs ${{rankColor}} shadow-xs">#${{t.rank}}</span>
              <span class="text-xs font-mono font-bold text-slate-500">${{t.imp > 0 ? '+' : ''}}${{t.imp}} IMP</span>
            </div>
            <h4 class="font-black text-slate-900 text-lg mb-1">${{t.team}}</h4>
            <span class="text-xs text-slate-500">${{currentLang === 'ar' ? 'الدوري الرسمي لكأس الأردن' : 'Official Jordan Cup League'}}</span>
          </div>

          <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-600">${{currentLang === 'ar' ? 'مجموع النقاط:' : 'Total V.P:'}}</span>
            <span class="text-lg font-black font-mono text-emerald-700">${{t.vp.toFixed(2)}}</span>
          </div>
        `;
        container.appendChild(card);
      }});
    }}"""

replacement = """    // Render Jordan Cup Cards (With Full Player Rosters)
    function renderJordanCup() {{
      const container = document.getElementById('jordanCupCards');
      container.innerHTML = '';

      jordanCupData.teams.forEach(t => {{
        const card = document.createElement('div');
        card.className = 'bg-white p-5 rounded-2xl border border-slate-200 hover:border-emerald-400 hover:shadow-md transition-all flex flex-col justify-between';
        
        let rankColor = 'bg-slate-200 text-slate-800';
        if (t.rank === 1) rankColor = 'badge-rank-1 font-black';
        else if (t.rank === 2) rankColor = 'badge-rank-2 font-black';
        else if (t.rank === 3) rankColor = 'badge-rank-3 font-black';

        const rosterHtml = (t.roster && t.roster.length > 0) ? `
          <div class="mt-3 pt-3 border-t border-slate-100">
            <span class="block text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">${{currentLang === 'ar' ? 'تشكيلة الفريق (اللاعبون):' : 'Team Roster / Players:'}}</span>
            <div class="flex flex-wrap gap-1">
              ${{t.roster.map(p => `<span class="text-[11px] font-medium px-2 py-0.5 rounded-md bg-slate-100 hover:bg-emerald-50 hover:text-emerald-800 text-slate-700 transition-colors">${{p}}</span>`).join('')}}
            </div>
          </div>
        ` : '';

        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="w-8 h-8 rounded-xl flex items-center justify-center text-xs ${{rankColor}} shadow-xs">#${{t.rank}}</span>
              <span class="text-xs font-mono font-bold text-slate-500">${{t.imp > 0 ? '+' : ''}}${{t.imp}} IMP</span>
            </div>
            <h4 class="font-black text-slate-900 text-lg mb-1">${{t.team}}</h4>
            <span class="text-xs text-slate-500">${{currentLang === 'ar' ? 'الدوري الرسمي لكأس الأردن' : 'Official Jordan Cup League'}}</span>
            ${{rosterHtml}}
          </div>

          <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-600">${{currentLang === 'ar' ? 'مجموع النقاط:' : 'Total V.P:'}}</span>
            <span class="text-lg font-black font-mono text-emerald-700">${{t.vp.toFixed(2)}}</span>
          </div>
        `;
        container.appendChild(card);
      }});
    }}"""

# Ensure file loading in build_site uses base_dir
code = code.replace("with open('public/data/", "import os\\nbase_dir = os.path.dirname(os.path.abspath(__file__))\\nwith open(os.path.join(base_dir, 'public/data/")
code = code.replace("with open('index.html'", "with open(os.path.join(base_dir, 'index.html')")

if target in code:
    code = code.replace(target, replacement)
    with open(build_site_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("SUCCESS: Roster rendering added and paths fixed!")
else:
    print("ERROR: Target block not found in build_site.py")
