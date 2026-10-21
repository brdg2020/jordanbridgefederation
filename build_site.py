import json
import os

with open('/Users/erdem/.gemini/antigravity/scratch/jbf-website/public/data/festival2026.json', 'r', encoding='utf-8') as f:
    fest_data = json.load(f)

with open('/Users/erdem/.gemini/antigravity/scratch/jbf-website/public/data/jordancup2026.json', 'r', encoding='utf-8') as f:
    cup_data = json.load(f)

with open('/Users/erdem/.gemini/antigravity/scratch/jbf-website/public/data/committee.json', 'r', encoding='utf-8') as f:
    comm_data = json.load(f)

fest_json_str = json.dumps(fest_data, ensure_ascii=False)
cup_json_str = json.dumps(cup_data, ensure_ascii=False)
comm_json_str = json.dumps(comm_data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jordan Bridge Federation | الاتحاد الأردني للبريدج</title>
  <meta name="description" content="Official Portal of the Jordan Bridge Federation (JBF). Tournaments, live Vugraph scores, Jordan Bridge Festival, Jordan Cup, bylaws, and community news.">
  <link rel="canonical" href="https://jordanbridgefederation.com/">
  
  <!-- Favicon & Fonts -->
  <link rel="icon" type="image/jpeg" href="public/jbf_logo.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800&family=Cinzel:wght@600;700;800&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#f0f7ff',
              100: '#e0effe',
              500: '#0284c7',
              600: '#0369a1',
              700: '#075985',
              800: '#0c4a6e',
              900: '#082f49',
              gold: '#d97706',
              jordanRed: '#ce1126',
              jordanGreen: '#007a3d',
              jordanBlack: '#000000'
            }}
          }},
          fontFamily: {{
            sans: ['Outfit', 'sans-serif'],
            arabic: ['Cairo', 'sans-serif'],
            display: ['Cinzel', 'serif']
          }}
        }}
      }}
    }}
  </script>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    [dir="rtl"] {{
      font-family: 'Cairo', sans-serif;
    }}
    .jordan-stripe {{
      height: 4px;
      background: linear-gradient(90deg, #000000 0%, #000000 33%, #ffffff 33%, #ffffff 66%, #007a3d 66%, #007a3d 100%);
      position: relative;
    }}
    .jordan-stripe::after {{
      content: '';
      position: absolute;
      left: 0;
      top: -2px;
      width: 0;
      height: 0;
      border-top: 4px solid transparent;
      border-bottom: 4px solid transparent;
      border-left: 12px solid #ce1126;
    }}
    .glass-card {{
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(226, 232, 240, 0.8);
    }}
    .badge-rank-1 {{ background: linear-gradient(135deg, #fef3c7, #fde68a); color: #92400e; border: 1px solid #f59e0b; }}
    .badge-rank-2 {{ background: linear-gradient(135deg, #f1f5f9, #e2e8f0); color: #334155; border: 1px solid #94a3b8; }}
    .badge-rank-3 {{ background: linear-gradient(135deg, #ffedd5, #fed7aa); color: #9a3412; border: 1px solid #f97316; }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased font-sans flex flex-col min-h-screen" id="bodyRoot">

  <!-- TOP STRIPE (Jordan Colors) -->
  <div class="h-1.5 w-full flex">
    <div class="flex-1 bg-black"></div>
    <div class="flex-1 bg-white"></div>
    <div class="flex-1 bg-emerald-700"></div>
    <div class="w-12 bg-red-600"></div>
  </div>

  <!-- HEADER -->
  <header class="sticky top-0 z-50 bg-white/95 backdrop-blur shadow-sm border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      
      <!-- Brand Logo & Title -->
      <a href="#" class="flex items-center gap-3.5 group">
        <img src="public/jbf_logo.jpg" alt="Jordan Bridge Federation Logo" class="h-14 w-auto object-contain rounded-lg shadow-sm border border-slate-200 group-hover:scale-105 transition-transform duration-200">
        <div>
          <span class="block text-lg sm:text-xl font-bold tracking-tight text-slate-900 group-hover:text-sky-700 transition-colors" data-en="Jordan Bridge Federation" data-ar="الاتحاد الأردني للبريدج">Jordan Bridge Federation</span>
          <span class="block text-xs font-semibold uppercase tracking-wider text-slate-500" data-en="Hashemite Kingdom of Jordan • JOC Affiliate" data-ar="المملكة الأردنية الهاشمية • تحت مظلة اللجنة الأولمبية">Hashemite Kingdom of Jordan • JOC Affiliate</span>
        </div>
      </a>

      <!-- Navigation & Language Switcher -->
      <div class="flex items-center gap-4 sm:gap-6">
        <nav class="hidden md:flex items-center gap-6 text-sm font-semibold text-slate-600">
          <a href="#scores" class="hover:text-sky-700 transition-colors" data-en="Live Scores & Results" data-ar="النتائج والسكور">Live Scores & Results</a>
          <a href="#jordancup" class="hover:text-sky-700 transition-colors" data-en="Jordan Cup" data-ar="كأس الأردن">Jordan Cup</a>
          <a href="#documents" class="hover:text-sky-700 transition-colors" data-en="Documents & Bylaws" data-ar="اللوائح والأنظمة">Documents & Bylaws</a>
          <a href="#committee" class="hover:text-sky-700 transition-colors" data-en="Committee" data-ar="مجلس الإدارة">Committee</a>
          <a href="#venue" class="hover:text-sky-700 transition-colors" data-en="Venue & Contact" data-ar="المقر والتواصل">Venue & Contact</a>
        </nav>

        <!-- Language Switcher Button -->
        <button id="langToggleBtn" onclick="toggleLanguage()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold border border-slate-300 bg-slate-100 hover:bg-slate-200 text-slate-800 transition-all shadow-xs">
          <i data-lucide="globe" class="w-3.5 h-3.5"></i>
          <span id="langLabel">العربية</span>
        </button>
      </div>

    </div>
  </header>

  <!-- HERO SECTION -->
  <section class="relative bg-gradient-to-b from-sky-900 via-sky-800 to-slate-900 text-white py-16 sm:py-24 overflow-hidden">
    <!-- Subtle Background Shapes -->
    <div class="absolute inset-0 opacity-10 pointer-events-none">
      <div class="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-sky-400 blur-3xl"></div>
      <div class="absolute -bottom-24 -right-24 w-96 h-96 rounded-full bg-emerald-400 blur-3xl"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
      <!-- Federation Pill -->
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 backdrop-blur border border-white/20 text-xs sm:text-sm font-semibold tracking-wide text-sky-200 mb-6">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span data-en="Official National Federation • Founded 1980s • Amman, Jordan" data-ar="الاتحاد الوطني الرسمي للبريدج • عمان، المملكة الأردنية الهاشمية">Official National Federation • Founded 1980s • Amman, Jordan</span>
      </div>

      <h1 class="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight max-w-4xl mx-auto leading-tight mb-6">
        <span data-en="The Home of Contract Bridge in Jordan" data-ar="المقر الرسمي لرياضة البريدج في الأردن">The Home of Contract Bridge in Jordan</span>
      </h1>

      <p class="text-base sm:text-lg text-sky-100/90 max-w-2xl mx-auto mb-10 leading-relaxed" data-en="Empowering minds, fostering international sportsmanship, and hosting premier tournaments under the Jordan Olympic Committee (JOC) and World Bridge Federation (WBF)." data-ar="تطوير رياضة الفكر والذكاء، ورعاية البطولات الدولية والمحلية تحت مظلة اللجنة الأولمبية الأردنية والاتحاد العالمي للبريدج (WBF).">
        Empowering minds, fostering international sportsmanship, and hosting premier tournaments under the Jordan Olympic Committee (JOC) and World Bridge Federation (WBF).
      </p>

      <div class="flex flex-wrap items-center justify-center gap-4">
        <a href="#scores" class="px-6 py-3.5 rounded-xl font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-lg shadow-amber-500/20 transition-all transform hover:-translate-y-0.5 inline-flex items-center gap-2">
          <i data-lucide="trophy" class="w-5 h-5"></i>
          <span data-en="Festival 2026 Live Scores" data-ar="نتائج مهرجان الأردن 2026">Festival 2026 Live Scores</span>
        </a>
        <a href="#jordancup" class="px-6 py-3.5 rounded-xl font-bold bg-white/10 hover:bg-white/20 text-white border border-white/20 backdrop-blur transition-all inline-flex items-center gap-2">
          <i data-lucide="award" class="w-5 h-5"></i>
          <span data-en="Jordan Cup 2026 Final" data-ar="نهائي كأس الأردن 2026">Jordan Cup 2026 Final</span>
        </a>
      </div>

      <!-- Quick Metrics Strip -->
      <div class="mt-14 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto pt-8 border-t border-white/15">
        <div class="text-center">
          <span class="block text-2xl sm:text-3xl font-extrabold text-white">42+</span>
          <span class="text-xs text-sky-200/80 font-medium" data-en="Festival Editions" data-ar="دورات المهرجان الدولي">Festival Editions</span>
        </div>
        <div class="text-center">
          <span class="block text-2xl sm:text-3xl font-extrabold text-white">24</span>
          <span class="text-xs text-sky-200/80 font-medium" data-en="Teams in 2026 Open" data-ar="فريقاً في بطولة 2026">Teams in 2026 Open</span>
        </div>
        <div class="text-center">
          <span class="block text-2xl sm:text-3xl font-extrabold text-white">WBF</span>
          <span class="text-xs text-sky-200/80 font-medium" data-en="Zone 4 (BFAME) Member" data-ar="عضو الاتحاد الدولي والآسيوي">Zone 4 (BFAME) Member</span>
        </div>
        <div class="text-center">
          <span class="block text-2xl sm:text-3xl font-extrabold text-white">100%</span>
          <span class="text-xs text-sky-200/80 font-medium" data-en="Mobile Optimized Vugraph" data-ar="سكور وعرض مباشر للموبايل">Mobile Optimized Vugraph</span>
        </div>
      </div>

    </div>
  </section>

  <!-- MAIN SCORING & VUGRAPH HUB SECTION -->
  <section id="scores" class="py-16 bg-slate-100 border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Section Header -->
      <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-4 border-b border-slate-300 gap-4">
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-sky-700 bg-sky-100 px-3 py-1 rounded-full inline-block mb-2" data-en="Vugraph & Live Standings" data-ar="عرض النتائج المباشرة والسكور">Vugraph & Live Standings</span>
          <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="Jordan Bridge Festival 2026 — Open Teams" data-ar="مهرجان الأردن الدولي للبريدج 2026 — الفرق المفتوحة">Jordan Bridge Festival 2026 — Open Teams</h2>
          <p class="text-sm text-slate-600 mt-1" data-en="Director: Waleed El Menyawi • 24 International & National Teams • 8 Complete Rounds" data-ar="مدير البطولة: وليد المنياوي • 24 فريقاً دولياً ومحلياً • 8 جولات كاملة">Director: Waleed El Menyawi • 24 International & National Teams • 8 Complete Rounds</p>
        </div>

        <!-- Search Bar -->
        <div class="w-full md:w-72">
          <div class="relative">
            <input type="text" id="teamSearchInput" oninput="filterTeams()" placeholder="Search team or score..." class="w-full pl-10 pr-4 py-2 text-sm bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 shadow-xs">
            <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5 top-3"></i>
          </div>
        </div>
      </div>

      <!-- Tab Buttons: Standings vs. Round-by-Round Breakdown -->
      <div class="flex items-center gap-2 mb-6 border-b border-slate-200 pb-2">
        <button id="btnTabStandings" onclick="switchFestivalTab('standings')" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-sky-700 text-white shadow-xs transition-all">
          <span data-en="Final Standings (Leaderboard)" data-ar="الترتيب النهائي للفرق">Final Standings (Leaderboard)</span>
        </button>
        <button id="btnTabRounds" onclick="switchFestivalTab('rounds')" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 transition-all">
          <span data-en="Round-by-Round Match Results" data-ar="نتائج المباريات جولة بجولة">Round-by-Round Match Results</span>
        </button>
        <a href="public/archive/jordanbridgefestival2026-teams.htm" target="_blank" class="ml-auto hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-sky-700 bg-white border border-slate-200 px-3 py-2 rounded-lg">
          <i data-lucide="file-code" class="w-3.5 h-3.5"></i>
          <span data-en="Raw Magic Contest Output" data-ar="ملف ماجيك كونتست الأصلي">Raw Magic Contest Output</span>
        </a>
      </div>

      <!-- TAB 1: STANDINGS TABLE -->
      <div id="tabStandingsContent" class="glass-card rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-sm">
            <thead>
              <tr class="bg-slate-900 text-white uppercase text-xs tracking-wider">
                <th class="py-3.5 px-4 text-center w-16" data-en="Rank" data-ar="الترتيب">Rank</th>
                <th class="py-3.5 px-4" data-en="Team Name" data-ar="اسم الفريق">Team Name</th>
                <th class="py-3.5 px-4 text-center w-28" data-en="Team #" data-ar="رقم الفريق">Team #</th>
                <th class="py-3.5 px-6 text-right w-36" data-en="Total V.P" data-ar="مجموع النقاط (VP)">Total V.P</th>
                <th class="py-3.5 px-4 text-center w-32" data-en="Status" data-ar="الحالة">Status</th>
              </tr>
            </thead>
            <tbody id="standingsTableBody" class="divide-y divide-slate-200 bg-white">
              <!-- Populated by JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- TAB 2: ROUND-BY-ROUND MATCHES -->
      <div id="tabRoundsContent" class="hidden">
        <!-- Round Selector Pills (1 to 8) -->
        <div class="flex items-center gap-2 overflow-x-auto pb-4 mb-4">
          <span class="text-xs font-bold text-slate-500 uppercase mr-2" data-en="Select Round:" data-ar="اختر الجولة:">Select Round:</span>
          <button onclick="renderRoundMatches(8)" class="round-pill-btn active px-4 py-2 rounded-xl text-xs font-bold bg-sky-700 text-white shadow-xs" data-round="8">Round 8 (Final)</button>
          <button onclick="renderRoundMatches(7)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="7">Round 7</button>
          <button onclick="renderRoundMatches(6)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="6">Round 6</button>
          <button onclick="renderRoundMatches(5)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="5">Round 5</button>
          <button onclick="renderRoundMatches(4)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="4">Round 4</button>
          <button onclick="renderRoundMatches(3)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="3">Round 3</button>
          <button onclick="renderRoundMatches(2)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="2">Round 2</button>
          <button onclick="renderRoundMatches(1)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="1">Round 1</button>
        </div>

        <!-- Matches Cards Grid -->
        <div id="roundMatchesContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Populated by JS -->
        </div>
      </div>

    </div>
  </section>

  <!-- JORDAN CUP SECTION (From Official Excel) -->
  <section id="jordancup" class="py-16 bg-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-4 border-b border-slate-200 gap-4">
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full inline-block mb-2" data-en="National League Championship" data-ar="بطولة الدوري الوطني">National League Championship</span>
          <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="Jordan Cup 2026 — Final League Standings" data-ar="كأس الأردن 2026 — الترتيب النهائي للدوري">Jordan Cup 2026 — Final League Standings</h2>
          <p class="text-sm text-slate-600 mt-1" data-en="Tournament Director: Raad Otoom • Verified Federation Excel Record" data-ar="مدير البطولة: رعد العتوم • السجل المعتمد من الاتحاد">Tournament Director: Raad Otoom • Verified Federation Excel Record</p>
        </div>

        <a href="public/archive/Jordan Cups 26 Final.xlsx" download class="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold bg-emerald-700 text-white hover:bg-emerald-600 shadow-sm transition-all self-start md:self-end">
          <i data-lucide="file-spreadsheet" class="w-4 h-4"></i>
          <span data-en="Download Official Excel" data-ar="تحميل ملف الإكسل الرسمي">Download Official Excel</span>
        </a>
      </div>

      <!-- Cup Standings Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="jordanCupCards">
        <!-- Populated by JS -->
      </div>

    </div>
  </section>

  <!-- OFFICIAL BYLAWS & DOCUMENTS (Kayıpsız Arşiv) -->
  <section id="documents" class="py-16 bg-slate-50 border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-2xl mx-auto mb-12">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-600 bg-slate-200 px-3 py-1 rounded-full inline-block mb-2" data-en="Governance & Regulations" data-ar="الأنظمة واللوائح والقرارات">Governance & Regulations</span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="Official Federation Documents" data-ar="الوثائق واللوائح الرسمية للاتحاد">Official Federation Documents</h2>
        <p class="text-sm text-slate-600 mt-2" data-en="Every constitution, tournament bulletin, and international alerting policy is archived and accessible for all members." data-ar="جميع الأنظمة الأساسية، نشرات المهرجان، وسياسات التنبيه المعتمدة متاحة لجميع الأعضاء واللاعبين.">
          Every constitution, tournament bulletin, and international alerting policy is archived and accessible for all members.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        
        <!-- Doc 1: By-Laws KP 220821 -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs hover:border-sky-400 hover:shadow-md transition-all flex flex-col justify-between">
          <div>
            <div class="w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center mb-4">
              <i data-lucide="scroll-text" class="w-5 h-5"></i>
            </div>
            <h3 class="font-bold text-slate-900 text-base mb-1" data-en="By-Laws Jordan Bridge Federation" data-ar="النظام الداخلي للاتحاد الأردني للبريدج">By-Laws Jordan Bridge Federation</h3>
            <p class="text-xs text-slate-500 mb-4" data-en="Official English constitution, governance rules, and executive board responsibilities." data-ar="النظام الأساسي باللغة الإنجليزية وقواعد الحوكمة ومسؤوليات مجلس الإدارة.">Official English constitution, governance rules, and executive board responsibilities.</p>
          </div>
          <a href="public/archive/BFAME Participation Record.pdf" target="_blank" class="inline-flex items-center justify-between text-xs font-bold text-sky-700 hover:text-sky-800 bg-sky-50 hover:bg-sky-100 px-4 py-2.5 rounded-xl transition-all">
            <span data-en="View Document (PDF)" data-ar="عرض الوثيقة (PDF)">View Document (PDF)</span>
            <i data-lucide="arrow-right" class="w-4 h-4"></i>
          </a>
        </div>

        <!-- Doc 2: WBF Alerting Policy -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs hover:border-sky-400 hover:shadow-md transition-all flex flex-col justify-between">
          <div>
            <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center mb-4">
              <i data-lucide="bell" class="w-5 h-5"></i>
            </div>
            <h3 class="font-bold text-slate-900 text-base mb-1" data-en="WBF Alerting Policy" data-ar="سياسة التنبيه المعتمدة من الاتحاد الدولي">WBF Alerting Policy</h3>
            <p class="text-xs text-slate-500 mb-4" data-en="Official World Bridge Federation regulations for bidding announcements, screens, and alerts." data-ar="لوائح الاتحاد العالمي للبريدج الرسمية للإعلانات والتنبيهات والشاشات أثناء اللعب.">Official World Bridge Federation regulations for bidding announcements, screens, and alerts.</p>
          </div>
          <a href="public/archive/WBF Alerting Policy.pdf" target="_blank" class="inline-flex items-center justify-between text-xs font-bold text-amber-700 hover:text-amber-800 bg-amber-50 hover:bg-amber-100 px-4 py-2.5 rounded-xl transition-all">
            <span data-en="Download Policy (PDF)" data-ar="تحميل السياسة (PDF)">Download Policy (PDF)</span>
            <i data-lucide="download" class="w-4 h-4"></i>
          </a>
        </div>

        <!-- Doc 3: Annual Festival Prospectus -->
        <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs hover:border-sky-400 hover:shadow-md transition-all flex flex-col justify-between">
          <div>
            <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center mb-4">
              <i data-lucide="file-text" class="w-5 h-5"></i>
            </div>
            <h3 class="font-bold text-slate-900 text-base mb-1" data-en="Annual Jordan Festival Prospectus" data-ar="دليل ولوائح مهرجان الأردن السنوي">Annual Jordan Festival Prospectus</h3>
            <p class="text-xs text-slate-500 mb-4" data-en="Tournament formats, masterpoints awards, match point schedules, and prize structures." data-ar="نظام البطولة، توزيع النقاط الذهبية، برامج اللعب، ومكافآت الفائزين.">Tournament formats, masterpoints awards, match point schedules, and prize structures.</p>
          </div>
          <a href="public/archive/Annual Jordan International Bridge Festival.docx" download class="inline-flex items-center justify-between text-xs font-bold text-emerald-700 hover:text-emerald-800 bg-emerald-50 hover:bg-emerald-100 px-4 py-2.5 rounded-xl transition-all">
            <span data-en="Download Prospectus (DOCX)" data-ar="تحميل الدليل (DOCX)">Download Prospectus (DOCX)</span>
            <i data-lucide="download" class="w-4 h-4"></i>
          </a>
        </div>

      </div>

    </div>
  </section>

  <!-- EXECUTIVE COMMITTEE & GENERAL AUTHORITY -->
  <section id="committee" class="py-16 bg-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-2xl mx-auto mb-12">
        <span class="text-xs font-bold uppercase tracking-wider text-sky-800 bg-sky-100 px-3 py-1 rounded-full inline-block mb-2" data-en="Leadership & Governance" data-ar="الإدارة والقيادة">Leadership & Governance</span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="General Authority & Executive Board" data-ar="الهيئة العامة ومجلس إدارة الاتحاد">General Authority & Executive Board</h2>
        <p class="text-sm text-slate-600 mt-2" data-en="Distinguished bridge leaders, patrons, and tournament officials dedicated to the development of mind sports in Jordan." data-ar="نخبة من رواد ومؤسسي رياضة البريدج والقائمين على تنظيم البطولات في المملكة الأردنية الهاشمية.">
          Distinguished bridge leaders, patrons, and tournament officials dedicated to the development of mind sports in Jordan.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4" id="committeeGrid">
        <!-- Populated by JS -->
      </div>

    </div>
  </section>

  <!-- SPONSORS & AFFILIATES -->
  <section class="py-12 bg-slate-50 border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <span class="text-xs font-bold uppercase tracking-wider text-slate-500 block mb-6" data-en="Official Federation Sponsors & Partners" data-ar="الرعاة الرسميون وشركاء الاتحاد">Official Federation Sponsors & Partners</span>
      
      <div class="flex flex-wrap items-center justify-center gap-8 sm:gap-14 opacity-80 hover:opacity-100 transition-opacity">
        <img src="public/tejari_bank.jpg" alt="Jordan Commercial Bank" class="h-12 w-auto object-contain grayscale hover:grayscale-0 transition-all">
        <img src="public/ethad_bank.jpg" alt="Bank Al Etihad" class="h-10 w-auto object-contain grayscale hover:grayscale-0 transition-all">
        <img src="public/capital_bank.jpg" alt="Capital Bank of Jordan" class="h-10 w-auto object-contain grayscale hover:grayscale-0 transition-all">
        <img src="public/national_paints.jpg" alt="National Paints" class="h-12 w-auto object-contain grayscale hover:grayscale-0 transition-all">
      </div>
    </div>
  </section>

  <!-- VENUE & CONTACT SECTION -->
  <section id="venue" class="py-16 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-red-700 bg-red-100 px-3 py-1 rounded-full inline-block mb-3" data-en="Location & Sessions" data-ar="المقر ومواعيد اللعب">Location & Sessions</span>
          <h2 class="text-3xl font-black text-slate-900 mb-4" data-en="Visit the Federation Club in Amman" data-ar="مقر الاتحاد الأردني للبريدج في عمان">Visit the Federation Club in Amman</h2>
          <p class="text-slate-600 text-sm leading-relaxed mb-6" data-en="Regular duplicate bridge sessions, pairs tournaments, masterclasses, and national team training take place at our official headquarters inside Prince Hamza Hall." data-ar="تقام بطولات الزوجي الأسبوعية والتدريبات الخاصة بالمنتخب الوطني والدورات التدريبية في مقرنا الرسمي بمدينة الحسين للشباب.">
            Regular duplicate bridge sessions, pairs tournaments, masterclasses, and national team training take place at our official headquarters inside Prince Hamza Hall.
          </p>

          <div class="space-y-4 text-sm text-slate-700">
            <div class="flex items-start gap-3">
              <i data-lucide="map-pin" class="w-5 h-5 text-red-600 shrink-0 mt-0.5"></i>
              <div>
                <strong class="block text-slate-900" data-en="Address:" data-ar="العنوان:">Address:</strong>
                <span data-en="Al Hussein Youth City, Prince Hamza Hall (Next to Sports Medicine Center), Sports City, Amman, Jordan" data-ar="مدينة الحسين للشباب، صالة الأمير حمزة (بجانب مركز الطب الرياضي)، المدينة الرياضية، عمان، الأردن">Al Hussein Youth City, Prince Hamza Hall (Next to Sports Medicine Center), Sports City, Amman, Jordan</span>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <i data-lucide="phone" class="w-5 h-5 text-emerald-700 shrink-0 mt-0.5"></i>
              <div>
                <strong class="block text-slate-900" data-en="Telephone & Mobile:" data-ar="أرقام الهواتف:">Telephone & Mobile:</strong>
                <span class="block" dir="ltr">+962 569 1057 (Office)</span>
                <span class="block" dir="ltr">+962 79 666 5565 (Federation Director)</span>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <i data-lucide="mail" class="w-5 h-5 text-sky-700 shrink-0 mt-0.5"></i>
              <div>
                <strong class="block text-slate-900" data-en="Official Email:" data-ar="البريد الإلكتروني:">Official Email:</strong>
                <a href="mailto:jo_bridge@yahoo.com" class="text-sky-700 font-semibold hover:underline">jo_bridge@yahoo.com</a>
              </div>
            </div>
          </div>
        </div>

        <!-- Venue Card -->
        <div class="bg-gradient-to-br from-slate-900 to-sky-950 text-white p-8 rounded-3xl shadow-xl border border-slate-800">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center border border-white/20">
              <i data-lucide="calendar" class="w-6 h-6 text-amber-400"></i>
            </div>
            <div>
              <h3 class="font-bold text-lg" data-en="Weekly Duplicate Sessions" data-ar="الجلسات الأسبوعية">Weekly Duplicate Sessions</h3>
              <span class="text-xs text-sky-300" data-en="Visitors & International Guests Welcome" data-ar="نرحب بالضيوف واللاعبين الدوليين">Visitors & International Guests Welcome</span>
            </div>
          </div>

          <p class="text-sm text-slate-300 leading-relaxed mb-6" data-en="Whether you are an experienced tournament master or looking to find a partner for the upcoming Jordan Festival, our directors and committee members are here to assist." data-ar="سواء كنت لاعباً محترفاً أو تبحث عن شريك للمشاركة في مهرجان الأردن القادم، فإن مدراء اللعب وأعضاء اللجنة في خدمتكم.">
            Whether you are an experienced tournament master or looking to find a partner for the upcoming Jordan Festival, our directors and committee members are here to assist.
          </p>

          <div class="p-4 rounded-xl bg-white/5 border border-white/10 text-xs text-slate-300 flex items-center justify-between">
            <span data-en="Sanctioned by WBF Zone 4" data-ar="معتمد من الاتحاد العالمي للبريدج">Sanctioned by WBF Zone 4</span>
            <span class="font-bold text-amber-400" data-en="Amman, Jordan" data-ar="عمان، الأردن">Amman, Jordan</span>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="bg-slate-950 text-slate-400 py-12 border-t border-slate-800 mt-auto text-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
      
      <div class="flex items-center gap-3">
        <img src="public/jbf_logo.jpg" alt="JBF" class="h-10 w-auto rounded border border-slate-700">
        <div>
          <span class="block text-slate-200 font-bold text-sm">Jordan Bridge Federation (JBF)</span>
          <span class="text-slate-500">© 2026 Hashemite Kingdom of Jordan. All Rights Reserved.</span>
        </div>
      </div>

      <div class="text-center sm:text-right">
        <p class="text-slate-400">Official Web Domain: <span class="text-amber-400 font-semibold">jordanbridgefederation.com</span></p>
        <p class="text-slate-600 mt-0.5">Olympic Sports City • Prince Hamza Hall • Amman</p>
      </div>

    </div>
  </footer>

  <!-- EMBEDDED REAL DATA & CLIENT CONTROLLER SCRIPT -->
  <script>
    const festivalData = {fest_json_str};
    const jordanCupData = {cup_json_str};
    const committeeData = {comm_json_str};

    let currentLang = 'en'; // 'en' or 'ar'
    let currentRound = 8;

    // Language Toggle
    function toggleLanguage() {{
      currentLang = (currentLang === 'en') ? 'ar' : 'en';
      const root = document.getElementById('bodyRoot');
      const langLabel = document.getElementById('langLabel');

      if (currentLang === 'ar') {{
        root.setAttribute('dir', 'rtl');
        langLabel.textContent = 'English';
      }} else {{
        root.setAttribute('dir', 'ltr');
        langLabel.textContent = 'العربية';
      }}

      // Update all translated tags
      document.querySelectorAll('[data-en]').forEach(el => {{
        const txt = el.getAttribute('data-' + currentLang);
        if (txt) {{
          el.textContent = txt;
        }}
      }});

      // Re-render components with translated dynamic text
      renderStandings(festivalData.standings);
      renderRoundMatches(currentRound);
      renderJordanCup();
      renderCommittee();
    }}

    // Switch between Festival Standings and Round Matches
    function switchFestivalTab(tab) {{
      const standingsContent = document.getElementById('tabStandingsContent');
      const roundsContent = document.getElementById('tabRoundsContent');
      const btnStandings = document.getElementById('btnTabStandings');
      const btnRounds = document.getElementById('btnTabRounds');

      if (tab === 'standings') {{
        standingsContent.classList.remove('hidden');
        roundsContent.classList.add('hidden');
        btnStandings.className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-sky-700 text-white shadow-xs transition-all';
        btnRounds.className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 transition-all';
      }} else {{
        standingsContent.classList.add('hidden');
        roundsContent.classList.remove('hidden');
        btnRounds.className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-sky-700 text-white shadow-xs transition-all';
        btnStandings.className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-white text-slate-700 border border-slate-300 hover:bg-slate-50 transition-all';
        renderRoundMatches(currentRound);
      }}
    }}

    // Render Standings
    function renderStandings(standingsList) {{
      const tbody = document.getElementById('standingsTableBody');
      tbody.innerHTML = '';

      standingsList.forEach((team) => {{
        let rankBadgeClass = 'bg-slate-100 text-slate-700';
        if (team.rank === 1) rankBadgeClass = 'badge-rank-1 font-bold';
        else if (team.rank === 2) rankBadgeClass = 'badge-rank-2 font-bold';
        else if (team.rank === 3) rankBadgeClass = 'badge-rank-3 font-bold';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-sky-50/60 transition-colors border-b border-slate-100';
        tr.innerHTML = `
          <td class="py-3 px-4 text-center">
            <span class="inline-flex items-center justify-center w-7 h-7 rounded-full text-xs ${{rankBadgeClass}}">
              ${{team.rank}}
            </span>
          </td>
          <td class="py-3 px-4 font-bold text-slate-900">
            ${{team.name}}
          </td>
          <td class="py-3 px-4 text-center text-xs text-slate-500 font-mono">
            #${{team.teamId}}
          </td>
          <td class="py-3 px-6 text-right font-extrabold text-sky-800 font-mono text-base">
            ${{team.score.toFixed(2)}}
          </td>
          <td class="py-3 px-4 text-center">
            ${{team.rank <= 3 ? '<span class="text-xs px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 font-bold">Podium</span>' : '<span class="text-xs text-slate-400">Finalist</span>'}}
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Filter teams by search input
    function filterTeams() {{
      const q = document.getElementById('teamSearchInput').value.toLowerCase().trim();
      const filtered = festivalData.standings.filter(t => 
        t.name.toLowerCase().includes(q) || t.score.toString().includes(q)
      );
      renderStandings(filtered);
    }}

    // Render Round Matches
    function renderRoundMatches(roundNum) {{
      currentRound = roundNum;
      
      // Update active button state
      document.querySelectorAll('.round-pill-btn').forEach(btn => {{
        if (parseInt(btn.getAttribute('data-round')) === roundNum) {{
          btn.className = 'round-pill-btn active px-4 py-2 rounded-xl text-xs font-bold bg-sky-700 text-white shadow-xs';
        }} else {{
          btn.className = 'round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300';
        }}
      }});

      const container = document.getElementById('roundMatchesContainer');
      container.innerHTML = '';
      const matches = festivalData.rounds[roundNum] || [];

      matches.forEach(m => {{
        const card = document.createElement('div');
        card.className = 'bg-white p-4 rounded-xl border border-slate-200 shadow-xs hover:border-sky-300 transition-all';
        
        const homeWon = m.homeTeam.vp > m.awayTeam.vp;
        const awayWon = m.awayTeam.vp > m.homeTeam.vp;

        card.innerHTML = `
          <div class="flex items-center justify-between text-xs text-slate-500 pb-2 mb-3 border-b border-slate-100">
            <span class="font-bold text-sky-700">Table ${{m.table}}</span>
            <span>IMP ${{m.homeTeam.imp}} - ${{m.awayTeam.imp}}</span>
          </div>

          <div class="space-y-2 text-sm">
            <div class="flex items-center justify-between ${{homeWon ? 'font-black text-slate-950' : 'text-slate-600'}}">
              <span class="truncate">${{m.homeTeam.name}}</span>
              <span class="px-2 py-0.5 rounded font-mono ${{homeWon ? 'bg-emerald-100 text-emerald-800 font-bold' : 'bg-slate-100 text-slate-600'}}">${{m.homeTeam.vp.toFixed(2)}}</span>
            </div>
            <div class="flex items-center justify-between ${{awayWon ? 'font-black text-slate-950' : 'text-slate-600'}}">
              <span class="truncate">${{m.awayTeam.name}}</span>
              <span class="px-2 py-0.5 rounded font-mono ${{awayWon ? 'bg-emerald-100 text-emerald-800 font-bold' : 'bg-slate-100 text-slate-600'}}">${{m.awayTeam.vp.toFixed(2)}}</span>
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // Render Jordan Cup Cards
    function renderJordanCup() {{
      const container = document.getElementById('jordanCupCards');
      container.innerHTML = '';

      jordanCupData.teams.forEach(t => {{
        const card = document.createElement('div');
        card.className = 'bg-slate-50 p-5 rounded-2xl border border-slate-200 hover:border-emerald-400 hover:shadow-sm transition-all flex flex-col justify-between';
        
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

          <div class="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-600">${{currentLang === 'ar' ? 'مجموع النقاط:' : 'Total V.P:'}}</span>
            <span class="text-lg font-black font-mono text-emerald-700">${{t.vp.toFixed(2)}}</span>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // Render Committee
    function renderCommittee() {{
      const container = document.getElementById('committeeGrid');
      container.innerHTML = '';

      committeeData.members.forEach(m => {{
        const card = document.createElement('div');
        card.className = 'bg-slate-50 p-4 rounded-xl border border-slate-200 text-sm hover:border-slate-300 transition-all';
        
        card.innerHTML = `
          <div class="flex items-start gap-3">
            <div class="w-9 h-9 rounded-full bg-sky-100 text-sky-800 font-bold flex items-center justify-center text-xs shrink-0">
              <i data-lucide="user" class="w-4 h-4"></i>
            </div>
            <div class="min-w-0 flex-1">
              <strong class="block text-slate-900 font-bold truncate text-sm">${{m.name}}</strong>
              <span class="block text-xs text-slate-500 truncate mt-0.5">${{m.email ? m.email : 'General Assembly'}}</span>
              ${{m.phone ? `<span class="block text-xs font-mono text-slate-400 mt-1" dir="ltr">${{m.phone}}</span>` : ''}}
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
      lucide.createIcons();
    }}

    // Initialization
    window.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();
      renderStandings(festivalData.standings);
      renderJordanCup();
      renderCommittee();
    }});
  </script>
</body>
</html>'''

with open('/Users/erdem/.gemini/antigravity/scratch/jbf-website/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated index.html successfully ({len(html_content)} bytes)")
