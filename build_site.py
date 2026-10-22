# -*- coding: utf-8 -*-
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# Load master data
with open(os.path.join(base_dir, 'public/data/jbf_master_data.json'), 'r', encoding='utf-8') as f:
    master_data = json.load(f)

# Load festival 2026 with rounds
with open(os.path.join(base_dir, 'public/data/festival2026.json'), 'r', encoding='utf-8') as f:
    fest2026_data = json.load(f)

# Load committee
with open(os.path.join(base_dir, 'public/data/committee.json'), 'r', encoding='utf-8') as f:
    comm_data = json.load(f)

# Load team directory
with open(os.path.join(base_dir, 'public/data/team_directory.json'), 'r', encoding='utf-8') as f:
    team_dir_data = json.load(f)
team_dir_json_str = json.dumps(team_dir_data, ensure_ascii=False)

master_json_str = json.dumps(master_data, ensure_ascii=False)
fest2026_json_str = json.dumps(fest2026_data, ensure_ascii=False)
comm_json_str = json.dumps(comm_data, ensure_ascii=False)

# List gallery images
gallery_dir = os.path.join(base_dir, 'public/gallery')
gallery_images = sorted(os.listdir(gallery_dir)) if os.path.exists(gallery_dir) else []
gallery_images = [img for img in gallery_images if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
gallery_json_str = json.dumps(gallery_images, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jordan Bridge Federation | الاتحاد الأردني للبريدج</title>
  <meta name="description" content="Official Portal of the Jordan Bridge Federation (JBF). Tournaments, live Vugraph scores, Jordan Bridge Festival, Jordan Cup, Excel spreadsheets, bylaws, committee, and archive.">
  <link rel="canonical" href="https://jordanbridgefederation.com/">
  
  <!-- Favicons & App Icons -->
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="shortcut icon" href="favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="public/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="public/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="public/apple-touch-icon.png">

  <!-- Open Graph / Social Sharing Meta -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://jordanbridgefederation.com/">
  <meta property="og:title" content="Jordan Bridge Federation | الاتحاد الأردني للبريدج">
  <meta property="og:description" content="Official Portal of the Jordan Bridge Federation. Tournaments, live results, Jordan Cup, and federation documents.">
  <meta property="og:image" content="https://jordanbridgefederation.com/public/jbf_logo.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://jordanbridgefederation.com/public/jbf_logo.jpg">

  <!-- Fonts -->
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
            }}
          }},
          fontFamily: {{
            sans: ['Outfit', 'Cairo', 'sans-serif'],
            serif: ['Cinzel', 'serif'],
            arabic: ['Cairo', 'sans-serif'],
          }}
        }}
      }}
    }};
  </script>
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    [dir="rtl"] {{
      font-family: 'Cairo', 'Outfit', sans-serif;
    }}
    .badge-rank-1 {{
      background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
      color: #ffffff;
      box-shadow: 0 4px 10px rgba(217, 119, 6, 0.35);
    }}
    .badge-rank-2 {{
      background: linear-gradient(135deg, #cbd5e1 0%, #94a3b8 100%);
      color: #0f172a;
      box-shadow: 0 4px 8px rgba(148, 163, 184, 0.3);
    }}
    .badge-rank-3 {{
      background: linear-gradient(135deg, #fdba74 0%, #ea580c 100%);
      color: #ffffff;
      box-shadow: 0 4px 8px rgba(234, 88, 12, 0.3);
    }}
    .glass-card {{
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
    }}
    /* Custom Sleek Scrollbar */
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: #f1f5f9;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #cbd5e1;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #94a3b8;
    }}
    /* Lightbox animation */
    .lightbox-enter {{
      opacity: 0;
      transform: scale(0.96);
    }}
    .lightbox-enter-active {{
      opacity: 1;
      transform: scale(1);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased font-sans flex flex-col min-h-screen" id="bodyRoot">

  <!-- TOP ROYAL EMIRATES PATRONAGE BANNER -->
  <div class="bg-slate-900 text-slate-300 text-xs py-2 px-4 border-b border-slate-800">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center gap-2">
        <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
        <span class="font-medium tracking-wide" data-en="Hashemite Kingdom of Jordan • Member of BFAME & World Bridge Federation (WBF)" data-ar="المملكة الأردنية الهاشمية • عضو الاتحاد الآسيوي والاتحاد العالمي للبريدج (WBF)">
          Hashemite Kingdom of Jordan • Member of BFAME & World Bridge Federation (WBF)
        </span>
      </div>
      <div class="flex items-center gap-4">
        <span class="hidden sm:inline text-slate-400" data-en="Official Federation Portal" data-ar="البوابة الرسمية المعتمدة">Official Federation Portal</span>
        <button onclick="openAdminModal()" class="text-[11px] font-bold text-amber-400 hover:text-amber-300 flex items-center gap-1 transition-colors">
          <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
          <span data-en="Admin Portal" data-ar="بوابة المشرف">Admin Portal</span>
        </button>
      </div>
    </div>
  </div>

  <!-- NAVIGATION BAR -->
  <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      
      <!-- Logo & Title -->
      <a href="#" class="flex items-center gap-3.5 group">
        <img src="public/jbf_logo.jpg" alt="Jordan Bridge Federation" class="h-14 w-auto rounded-md shadow-xs border border-slate-200 group-hover:scale-105 transition-transform duration-200">
        <div>
          <span class="text-xs uppercase tracking-widest font-extrabold text-amber-700 block" data-en="Jordan Bridge Federation" data-ar="الاتحاد الأردني للبريدج">Jordan Bridge Federation</span>
          <h1 class="text-base sm:text-lg font-black text-slate-900 tracking-tight" data-en="Official National Portal" data-ar="البوابة الوطنية الرسمية">Official National Portal</h1>
        </div>
      </a>

      <!-- Desktop Nav Links -->
      <nav class="hidden md:flex items-center gap-7 text-sm font-semibold text-slate-700">
        <a href="#scores" class="hover:text-sky-700 transition-colors" data-en="Festival Scores" data-ar="نتائج المهرجان">Festival Scores</a>
        <a href="#league" class="hover:text-sky-700 transition-colors text-emerald-700 flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span data-en="National Leagues & Cup" data-ar="الدوري الوطني وكأس الأردن">National Leagues & Cup</span>
        </a>
        <a href="#posters" class="hover:text-sky-700 transition-colors" data-en="Posters" data-ar="الملصقات">Posters</a>
        <a href="#gallery" class="hover:text-sky-700 transition-colors" data-en="Gallery" data-ar="الصور">Gallery</a>
        <a href="#documents" class="hover:text-sky-700 transition-colors" data-en="Archive" data-ar="الوثائق">Archive</a>
        <a href="#committee" class="hover:text-sky-700 transition-colors" data-en="Committee" data-ar="الإدارة">Committee</a>
      </nav>

      <!-- Language & Admin Action -->
      <div class="flex items-center gap-3">
        <button id="langToggleBtn" onclick="toggleLanguage()" class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-bold border border-slate-300 bg-slate-100 hover:bg-slate-200 text-slate-800 transition-all shadow-xs cursor-pointer">
          <i data-lucide="languages" class="w-4 h-4 text-sky-700"></i>
          <span id="langLabel">العربية</span>
        </button>

        <!-- Mobile Menu Toggle Button -->
        <button onclick="toggleMobileMenu()" class="md:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100 focus:outline-none">
          <i data-lucide="menu" class="w-6 h-6"></i>
        </button>
      </div>

    </div>

    <!-- Mobile Navigation Drawer -->
    <div id="mobileMenu" class="hidden md:hidden border-t border-slate-200 bg-white px-4 pt-3 pb-5 space-y-2 text-sm font-semibold shadow-lg">
      <a href="#scores" onclick="toggleMobileMenu()" class="block py-2 text-slate-700 hover:text-sky-700" data-en="Festival Scores" data-ar="نتائج المهرجان">Festival Scores</a>
      <a href="#league" onclick="toggleMobileMenu()" class="block py-2 text-emerald-700 font-bold" data-en="National Leagues & Cup" data-ar="الدوري الوطني وكأس الأردن">National Leagues & Cup</a>
      <a href="#posters" onclick="toggleMobileMenu()" class="block py-2 text-slate-700 hover:text-sky-700" data-en="Official Posters" data-ar="الملصقات الرسمية">Official Posters</a>
      <a href="#gallery" onclick="toggleMobileMenu()" class="block py-2 text-slate-700 hover:text-sky-700" data-en="Photo Gallery" data-ar="معرض الصور">Photo Gallery</a>
      <a href="#documents" onclick="toggleMobileMenu()" class="block py-2 text-slate-700 hover:text-sky-700" data-en="Bylaws & Archive" data-ar="الأنظمة والأرشيف">Bylaws & Archive</a>
      <a href="#committee" onclick="toggleMobileMenu()" class="block py-2 text-slate-700 hover:text-sky-700" data-en="Executive Committee" data-ar="الهيئة الإدارية">Executive Committee</a>
      <div class="pt-2 border-t border-slate-100 flex items-center justify-between">
        <button onclick="openAdminModal(); toggleMobileMenu();" class="text-xs font-bold text-amber-700 flex items-center gap-1.5 py-1">
          <i data-lucide="shield-check" class="w-4 h-4"></i>
          <span data-en="Open Admin Data Entry" data-ar="فتح لوحة إدخال البيانات">Open Admin Data Entry</span>
        </button>
      </div>
    </div>
  </header>

  <!-- MEMORIAL & CONDOLENCE SECTION: MR. ISSAM HALIM SALFITI -->
  <section id="memorial" class="bg-gradient-to-r from-amber-50 via-slate-50 to-amber-50 border-b border-amber-200/80 py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row items-center gap-8 bg-white p-6 sm:p-8 rounded-3xl border border-amber-200 shadow-md">
        
        <!-- Large Portrait with Gold Frame & Lightbox Zoom -->
        <div class="relative group shrink-0 cursor-pointer" onclick="openLightbox('public/images/issam_01.jpg', 'In Loving Memory: Mr. Issam Halim Salfiti (السيد عصام حليم السلفيتي رحمه الله)')">
          <img src="public/images/issam_01.jpg" alt="Mr. Issam Halim Salfiti" class="w-48 h-48 sm:w-56 sm:h-56 object-cover rounded-2xl border-4 border-amber-400 shadow-xl group-hover:scale-102 transition-transform duration-300">
          <div class="absolute inset-0 bg-slate-950/20 opacity-0 group-hover:opacity-100 rounded-2xl transition-opacity flex items-center justify-center text-white">
            <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900/80 backdrop-blur-md text-xs font-bold border border-white/20">
              <i data-lucide="zoom-in" class="w-4 h-4 text-amber-400"></i>
              <span data-en="Zoom Portrait" data-ar="تكبير الصورة">Zoom Portrait</span>
            </span>
          </div>
        </div>

        <!-- Obituary Text Content -->
        <div class="flex-1 text-center md:text-left">
          <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-slate-900 text-amber-300 text-xs font-bold mb-3 border border-amber-500/30">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            <span data-en="Federation Memorial & Obituary Tribute" data-ar="نعي وتأبين الاتحاد الأردني للبريدج">Federation Memorial & Obituary Tribute</span>
          </div>
          
          <h2 class="text-xl sm:text-2xl font-black text-slate-900 tracking-tight" data-en="In Loving Memory of Mr. Issam Halim Salfiti" data-ar="نعي الصديق العزيز والراعي الكريم السيد عصام حليم السلفيتي رحمه الله">
            In Loving Memory of Mr. Issam Halim Salfiti (عصام حليم السلفيتي)
          </h2>

          <!-- Arabic Official Obituary -->
          <p class="text-xs sm:text-sm text-slate-700 mt-2.5 leading-relaxed font-arabic" dir="rtl">
            ببالغ الحزن والأسى، ينعى الاتحاد الأردني للبريدج الصديق العزيز، <strong>السيد عصام حليم السلفيتي</strong> الذي انتقل إلى رحمة الله تعالى بعد صراع مع المرض. لقد كان الفقيد من خيرة أبناء الأردن، إنسانًا نادرًا في أخلاقه وكرمه وعطائه، محبًا للناس وداعمًا للجميع، وكان دائمًا إلى جانب الجمعيات والأندية والاتحادات الرياضية. وباسم أسرة الاتحاد الأردني للبريدج، رئيسًا وأعضاءً ولاعبين، نتقدم بأصدق مشاعر التعزية والمواساة إلى عائلة الفقيد الكريمة، سائلين المولى عز وجل أن يتغمده بواسع رحمته ويسكنه فسيح جناته. رحم الله عصام السلفيتي، وأبقى ذكراه العطرة وأثره الطيب بين الناس.
          </p>

          <!-- English Tribute -->
          <p class="text-xs sm:text-sm text-slate-600 mt-2 leading-relaxed" data-en="In deep grief and sorrow, the Jordan Bridge Federation mourns the passing of our dear friend, pillar, and patron, Mr. Issam Halim Salfiti. The deceased was among Jordan's finest sons—a rare individual of noble character, boundless generosity, and heartfelt support for sports, clubs, and charitable foundations across the Kingdom. May his soul rest in eternal peace." data-ar="">
            In deep grief and sorrow, the Jordan Bridge Federation mourns the passing of our dear friend, pillar, and patron, Mr. Issam Halim Salfiti. The deceased was among Jordan's finest sons—a rare individual of noble character, boundless generosity, and heartfelt support for sports, clubs, and charitable foundations across the Kingdom. May his soul rest in eternal peace.
          </p>
        </div>

      </div>
    </div>
  </section>

  <!-- HERO BANNER -->
  <section class="relative bg-gradient-to-b from-sky-950 via-sky-900 to-slate-900 text-white py-16 sm:py-20 overflow-hidden">
    <div class="absolute inset-0 opacity-10 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:20px_20px]"></div>
    
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-sky-800/60 border border-sky-400/30 text-sky-200 text-xs font-bold mb-6">
        <i data-lucide="trophy" class="w-4 h-4 text-amber-400"></i>
        <span data-en="42nd Jordan International Bridge Festival & Official League" data-ar="مهرجان الأردن الدولي الـ 42 للبريدج والدوري الرسمي">42nd Jordan International Bridge Festival & Official League</span>
      </div>

      <h1 class="text-3xl sm:text-5xl font-black tracking-tight max-w-4xl mx-auto leading-tight" data-en="The Official Gateway to Bridge Excellence in the Hashemite Kingdom" data-ar="البوابة الرسمية لرياضة وفكر البريدج في المملكة الأردنية الهاشمية">
        The Official Gateway to Bridge Excellence in the Hashemite Kingdom
      </h1>

      <p class="mt-4 text-base sm:text-lg text-sky-100/80 max-w-3xl mx-auto font-light leading-relaxed" data-en="Live Vugraph scoring, official league cross-tables, tournament bulletins, international regulations, and national championship archives." data-ar="النتائج الحية والمباشرة، جداول الدوري الرسمي، نشرات المهرجانات، اللوائح والأنظمة الدولية، وأرشيف البطولات الوطنية.">
        Live Vugraph scoring, official league cross-tables, tournament bulletins, international regulations, and national championship archives.
      </p>

      <!-- Key Quick Stats -->
      <div class="mt-10 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
        <div class="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/10">
          <span class="text-2xl font-black text-amber-400 font-mono">42</span>
          <span class="block text-xs text-sky-200 uppercase font-semibold mt-1" data-en="Festival Editions" data-ar="نسخة من المهرجان الدولي">Festival Editions</span>
        </div>
        <div class="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/10">
          <span class="text-2xl font-black text-emerald-400 font-mono">8</span>
          <span class="block text-xs text-sky-200 uppercase font-semibold mt-1" data-en="Jordan Cup Clubs" data-ar="أندية بكأس الأردن">Jordan Cup Clubs</span>
        </div>
        <div class="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/10">
          <span class="text-2xl font-black text-sky-300 font-mono">100%</span>
          <span class="block text-xs text-sky-200 uppercase font-semibold mt-1" data-en="In-Browser Excels" data-ar="جداول إكسل تفاعلية">In-Browser Excels</span>
        </div>
        <div class="bg-white/10 backdrop-blur-md p-4 rounded-2xl border border-white/10">
          <span class="text-2xl font-black text-purple-300 font-mono">14</span>
          <span class="block text-xs text-sky-200 uppercase font-semibold mt-1" data-en="Archived Documents" data-ar="وثائق ولوائح رسمية">Archived Documents</span>
        </div>
      </div>

      <!-- Quick Action Buttons -->
      <div class="mt-10 flex flex-wrap items-center justify-center gap-4">
        <a href="#scores" class="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-sm transition-all shadow-md flex items-center gap-2">
          <i data-lucide="activity" class="w-4 h-4"></i>
          <span data-en="View Festival Standings" data-ar="استعراض نتائج المهرجان">View Festival Standings</span>
        </a>
        <a href="#league" class="px-6 py-3 rounded-xl bg-white/15 hover:bg-white/25 border border-white/20 text-white font-bold text-sm transition-all backdrop-blur-md flex items-center gap-2">
          <i data-lucide="table-2" class="w-4 h-4 text-emerald-400"></i>
          <span data-en="Open Live Spreadsheets" data-ar="فتح جداول الدوري المباشرة">Open Live Spreadsheets</span>
        </a>
      </div>
    </div>
  </section>

  <!-- OLYMPIC PATRONAGE: HRH PRINCE FEISAL IBN AL-HUSSEIN -->
  <section class="py-8 bg-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row items-center gap-6 p-6 rounded-2xl bg-slate-50 border border-slate-200 text-center sm:text-left shadow-xs">
        <div class="relative group cursor-pointer shrink-0" onclick="openLightbox('public/images/feisal.jpg', 'HRH Prince Feisal Ibn Al-Hussein - President of Jordan Olympic Committee')">
          <img src="public/images/feisal.jpg" alt="HRH Prince Feisal Ibn Al-Hussein" class="w-20 h-28 sm:w-24 sm:h-32 object-cover rounded-xl border-2 border-slate-300 shadow-sm group-hover:border-sky-500 transition-all">
          <div class="absolute inset-0 bg-slate-900/30 opacity-0 group-hover:opacity-100 rounded-xl transition-opacity flex items-center justify-center text-white text-xs">
            <i data-lucide="zoom-in" class="w-4 h-4"></i>
          </div>
        </div>
        <div class="flex-1">
          <span class="text-xs font-bold uppercase tracking-wider text-sky-800 bg-sky-100 px-3 py-1 rounded-full inline-block mb-1.5" data-en="Jordan Olympic Committee (JOC)" data-ar="اللجنة الأولمبية الأردنية">Jordan Olympic Committee (JOC)</span>
          <h3 class="text-base sm:text-lg font-black text-slate-900" data-en="Royal Highness Prince Feisal Ibn Al-Hussein" data-ar="صاحب السمو الملكي الأمير فيصل بن الحسين المعظم">Royal Highness Prince Feisal Ibn Al-Hussein</h3>
          <p class="text-xs font-bold text-slate-500 uppercase tracking-wider" data-en="President, Jordan Olympic Committee" data-ar="رئيس اللجنة الأولمبية الأردنية">President, Jordan Olympic Committee</p>
          <blockquote class="mt-2 text-xs sm:text-sm text-slate-700 italic border-l-2 sm:border-l-4 border-amber-400 pl-3 py-0.5" data-en="&ldquo;Out of scratch sports achievements do not exist. Achievements are the products of big efforts, generous giving, sacrifices and high expenditures.&rdquo;" data-ar="&ldquo;الإنجازات الرياضية لا تأتي من فراغ، بل هي نتاج جهود كبيرة وعطاء سخي وتضحيات وإنفاق مدروس.&rdquo;">
            &ldquo;Out of scratch sports achievements do not exist. Achievements are the products of big efforts, generous giving, sacrifices and high expenditures.&rdquo;
          </blockquote>
        </div>
      </div>
    </div>
  </section>

  <!-- OFFICIAL FESTIVAL POSTERS & ANNOUNCEMENTS (WITH LIGHTBOX ZOOM) -->
  <section id="posters" class="py-14 bg-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-2xl mx-auto mb-10">
        <span class="text-xs font-bold uppercase tracking-wider text-sky-800 bg-sky-100 px-3 py-1 rounded-full inline-block mb-2" data-en="Official Announcements" data-ar="الإعلانات والملصقات الرسمية">Official Announcements</span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="42nd Festival Posters & Program" data-ar="ملصقات وبرنامج المهرجان الدولي الـ 42">42nd Festival Posters & Program</h2>
        <p class="text-sm text-slate-600 mt-2" data-en="Click on any poster to zoom in full-screen and read tournament schedules, entry conditions, and prizes." data-ar="انقر على أي ملصق لتكبيره بالكامل وقراءة الجدول الزمني وشروط المشاركة والجوائز.">
          Click on any poster to zoom in full-screen and read tournament schedules, entry conditions, and prizes.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
        
        <!-- Poster 1 -->
        <div class="group relative rounded-2xl overflow-hidden border border-slate-200 shadow-md hover:shadow-xl transition-all cursor-pointer bg-slate-900" onclick="openLightbox('public/images/JOR261.jpg', '42nd Jordan Bridge Festival - General Announcement')">
          <img src="public/images/JOR261.jpg" alt="42nd Jordan Bridge Festival - General Poster" class="w-full h-auto object-cover group-hover:scale-102 transition-transform duration-300">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent opacity-90 group-hover:opacity-100 transition-opacity flex items-end p-5">
            <div class="w-full flex items-center justify-between">
              <div>
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider" data-en="Official Announcement" data-ar="الإعلان الرسمي">Official Announcement</span>
                <h4 class="text-white font-black text-base" data-en="42nd Festival Schedule & Venue" data-ar="جدول ومواعيد المهرجان الـ 42">42nd Festival Schedule & Venue</h4>
              </div>
              <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/20 text-white backdrop-blur-md text-xs font-bold border border-white/30">
                <i data-lucide="zoom-in" class="w-4 h-4"></i>
                <span data-en="Zoom" data-ar="تكبير">Zoom</span>
              </span>
            </div>
          </div>
        </div>

        <!-- Poster 2 -->
        <div class="group relative rounded-2xl overflow-hidden border border-slate-200 shadow-md hover:shadow-xl transition-all cursor-pointer bg-slate-900" onclick="openLightbox('public/images/JOR_262.jpg', '42nd Jordan Bridge Festival - Tournament Regulations & Prizes')">
          <img src="public/images/JOR_262.jpg" alt="42nd Jordan Bridge Festival - Program Poster" class="w-full h-auto object-cover group-hover:scale-102 transition-transform duration-300">
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent opacity-90 group-hover:opacity-100 transition-opacity flex items-end p-5">
            <div class="w-full flex items-center justify-between">
              <div>
                <span class="text-xs font-bold text-amber-400 uppercase tracking-wider" data-en="Tournament Guidelines" data-ar="تعليمات وجوائز البطولة">Tournament Guidelines</span>
                <h4 class="text-white font-black text-base" data-en="Prizes, Teams & Pairs Breakdown" data-ar="تفاصيل الجوائز والفرق والزوجي">Prizes, Teams & Pairs Breakdown</h4>
              </div>
              <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/20 text-white backdrop-blur-md text-xs font-bold border border-white/30">
                <i data-lucide="zoom-in" class="w-4 h-4"></i>
                <span data-en="Zoom" data-ar="تكبير">Zoom</span>
              </span>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>

  <!-- SECTION 1: FESTIVAL SCORES & ARCHIVE (2026, 2025, 2024, 2023) -->
  <section id="scores" class="py-16 bg-slate-100 border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Section Header -->
      <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-xs font-bold uppercase tracking-wider text-sky-800" data-en="Festival Standings & Archives" data-ar="نتائج وأرشيف مهرجانات الأردن">Festival Standings & Archives</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mt-1" id="festivalDisplayTitle">
            42nd Jordan Bridge Festival (2026) - Open Teams
          </h2>
          <p class="text-xs sm:text-sm text-slate-500 mt-1" id="festivalMetaInfo">
            Official Scoring • Tournament Director: Waleed El Menyawi (Egyptian Bridge Federation)
          </p>
        </div>

        <!-- Year Selector Buttons -->
        <div class="flex flex-wrap items-center gap-2 bg-white p-1.5 rounded-2xl border border-slate-300 shadow-xs">
          <button onclick="selectFestivalYear('2026')" id="btnYear2026" class="year-btn active px-3.5 py-1.5 rounded-xl text-xs font-bold bg-sky-700 text-white shadow-xs">2026 (42nd)</button>
          <button onclick="selectFestivalYear('2025')" id="btnYear2025" class="year-btn px-3.5 py-1.5 rounded-xl text-xs font-bold text-slate-700 hover:bg-slate-100">2025 (41st)</button>
          <button onclick="selectFestivalYear('2024')" id="btnYear2024" class="year-btn px-3.5 py-1.5 rounded-xl text-xs font-bold text-slate-700 hover:bg-slate-100">2024 (40th)</button>
          <button onclick="selectFestivalYear('2023')" id="btnYear2023" class="year-btn px-3.5 py-1.5 rounded-xl text-xs font-bold text-slate-700 hover:bg-slate-100">2023 (39th)</button>
        </div>
      </div>

      <!-- Controls & Subtabs Bar -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        
        <!-- Tab Selector (For 2026) -->
        <div class="inline-flex p-1 bg-white border border-slate-300 rounded-2xl shadow-xs" id="subtabContainer">
          <button id="btnTabStandings" onclick="switchFestivalSubtab('standings')" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-sky-700 text-white shadow-xs transition-all">
            <span data-en="Final Standings" data-ar="الترتيب النهائي">Final Standings</span>
          </button>
          <button id="btnTabRounds" onclick="switchFestivalSubtab('rounds')" class="px-5 py-2.5 rounded-xl font-bold text-sm bg-white text-slate-700 hover:bg-slate-50 transition-all">
            <span data-en="Round Matches (2026)" data-ar="مباريات الجولات (2026)">Round Matches (2026)</span>
          </button>
        </div>

        <!-- Search Bar -->
        <div class="relative w-full sm:w-72">
          <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-3"></i>
          <input type="text" id="teamSearchInput" oninput="filterFestivalTeams()" placeholder="Search team or score..." class="w-full pl-10 pr-4 py-2 text-sm bg-white border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 shadow-xs">
        </div>

      </div>

      <!-- STANDINGS TABLE CONTENT -->
      <div id="tabStandingsContent" class="glass-card rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-sm">
            <thead>
              <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                <th class="py-3.5 px-4 text-center font-bold" data-en="Rank" data-ar="المركز">Rank</th>
                <th class="py-3.5 px-4 font-bold" data-en="Team Name" data-ar="اسم الفريق">Team Name</th>
                <th class="py-3.5 px-4 text-center font-bold" data-en="Team #" data-ar="رقم الفريق">Team #</th>
                <th class="py-3.5 px-6 text-right font-bold" data-en="Victory Points (V.P)" data-ar="النقاط (V.P)">Victory Points (V.P)</th>
                <th class="py-3.5 px-4 text-center font-bold" data-en="Status" data-ar="الحالة">Status</th>
              </tr>
            </thead>
            <tbody id="standingsTableBody" class="divide-y divide-slate-200 bg-white">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- ROUND-BY-ROUND MATCHES CONTENT (2026) -->
      <div id="tabRoundsContent" class="hidden">
        
        <!-- Round Pills -->
        <div class="flex items-center gap-2 overflow-x-auto pb-4 mb-4">
          <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mr-2" data-en="Rounds:" data-ar="الجولات:">Rounds:</span>
          <button onclick="renderRoundMatches(8)" class="round-pill-btn active px-4 py-2 rounded-xl text-xs font-bold bg-sky-700 text-white shadow-xs" data-round="8">Round 8 (Final)</button>
          <button onclick="renderRoundMatches(7)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="7">Round 7</button>
          <button onclick="renderRoundMatches(6)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="6">Round 6</button>
          <button onclick="renderRoundMatches(5)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="5">Round 5</button>
          <button onclick="renderRoundMatches(4)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="4">Round 4</button>
          <button onclick="renderRoundMatches(3)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="3">Round 3</button>
          <button onclick="renderRoundMatches(2)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="2">Round 2</button>
          <button onclick="renderRoundMatches(1)" class="round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300" data-round="1">Round 1</button>
        </div>

        <!-- Matches Grid -->
        <div id="roundMatchesContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Dynamically populated -->
        </div>

      </div>

    </div>
  </section>

  <!-- SECTION 2: OFFICIAL LEAGUE SPREADSHEETS & SPREADSHEET VIEWER -->
  <section id="league" class="py-16 bg-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-3xl mx-auto mb-10">
        <span class="text-xs font-bold uppercase tracking-wider text-emerald-800 bg-emerald-100 px-3 py-1 rounded-full inline-block mb-2" data-en="Interactive In-Browser Spreadsheets" data-ar="جداول الدوري المباشرة دون الحاجة للتحميل">Interactive In-Browser Spreadsheets</span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="Official National League Cross-Tables & Matrices" data-ar="مصفوفات وجداول ترتيب الدوري الوطني الرسمي">Official National League Cross-Tables & Matrices</h2>
        <p class="text-sm text-slate-600 mt-2" data-en="Explore every round score, VP, IMP differential, and complete player rosters directly in your browser. Hover over any team name to reveal player line-ups." data-ar="استعرض نتائج كل جولة، نقاط الفيكتوري بوينت، وفارق الإمب وتشكيلة اللاعبين مباشرة دون الحاجة لتحميل ملفات. مرر الفأرة فوق أي فريق لرؤية كشف اللاعبين.">
          Explore every round score, VP, IMP differential, and complete player rosters directly in your browser. Hover over any team name to reveal player line-ups.
        </p>
      </div>

      <!-- Spreadsheet Selector Tabs: 3 Main Official Tournament Series -->
      <div class="flex flex-wrap items-center justify-center gap-2.5 mb-8">
        <button onclick="switchSpreadsheet('cup26')" id="tabBtn_cup26" class="sheet-tab-btn active px-5 py-2.5 rounded-xl font-bold text-xs sm:text-sm bg-emerald-700 text-white shadow-xs transition-all flex items-center gap-2">
          <i data-lucide="trophy" class="w-4 h-4 text-amber-300"></i>
          <span data-en="Jordan Cup 2026 (Premier League)" data-ar="كأس الأردن 2026 (الدوري الممتاز)">Jordan Cup 2026 (Premier League)</span>
        </button>
        <button onclick="switchSpreadsheet('cup25')" id="tabBtn_cup25" class="sheet-tab-btn px-5 py-2.5 rounded-xl font-bold text-xs sm:text-sm bg-slate-100 text-slate-700 hover:bg-slate-200 transition-all flex items-center gap-2">
          <i data-lucide="archive" class="w-4 h-4 text-slate-500"></i>
          <span data-en="Jordan Cup 2025 Final" data-ar="نهائي كأس الأردن 2025">Jordan Cup 2025 Final</span>
        </button>
        <button onclick="switchSpreadsheet('mix25')" id="tabBtn_mix25" class="sheet-tab-btn px-5 py-2.5 rounded-xl font-bold text-xs sm:text-sm bg-slate-100 text-slate-700 hover:bg-slate-200 transition-all flex items-center gap-2">
          <i data-lucide="users" class="w-4 h-4 text-indigo-600"></i>
          <span data-en="Mixed Selection League 2025" data-ar="تصفيات الزوجي المختلط 2025">Mixed Selection League 2025</span>
        </button>
      </div>

      <!-- TOURNAMENT 1: JORDAN CUP 2026 (UNIFIED: MATRIX, MATCH SCORES & CLUBS) -->
      <div id="view_cup26" class="sheet-view">
        
        <!-- Controls & Sub-view Switcher Bar -->
        <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200 mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-xs font-bold text-slate-500 uppercase tracking-wider mr-1" data-en="Views:" data-ar="طريقة العرض:">Views:</span>
            <button onclick="switchCup26Subtab('matrix')" id="cup26SubBtn_matrix" class="cup26-subtab active px-3.5 py-1.5 rounded-lg text-xs font-bold bg-emerald-700 text-white shadow-xs transition-all flex items-center gap-1.5">
              <i data-lucide="grid" class="w-3.5 h-3.5"></i>
              <span data-en="Cross-Table Matrix" data-ar="جدول ومصفوفة الترتيب">Cross-Table Matrix</span>
            </button>
            <button onclick="switchCup26Subtab('sched')" id="cup26SubBtn_sched" class="cup26-subtab px-3.5 py-1.5 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-200 hover:bg-slate-100 transition-all flex items-center gap-1.5">
              <i data-lucide="calendar" class="w-3.5 h-3.5"></i>
              <span data-en="Match Scores & Pairings" data-ar="نتائج ومباريات الجولات">Match Scores & Pairings</span>
            </button>
            <button onclick="switchCup26Subtab('clubs')" id="cup26SubBtn_clubs" class="cup26-subtab px-3.5 py-1.5 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-200 hover:bg-slate-100 transition-all flex items-center gap-1.5">
              <i data-lucide="shield" class="w-3.5 h-3.5"></i>
              <span data-en="Participating Clubs" data-ar="الأندية المشاركة">Participating Clubs</span>
            </button>
          </div>

          <div class="flex items-center gap-2">
            <a href="public/archive/Jordan Cups 26 Final.xlsx" download class="inline-flex items-center gap-1.5 font-bold text-emerald-700 hover:text-emerald-800 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-xs text-xs">
              <i data-lucide="download" class="w-3.5 h-3.5"></i>
              <span>Final Results (.xlsx)</span>
            </a>
            <a href="public/archive/Jordan Cups 26 schedule.xlsx" download class="inline-flex items-center gap-1.5 font-bold text-slate-600 hover:text-slate-800 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-xs text-xs">
              <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5"></i>
              <span>Schedule (.xlsx)</span>
            </a>
          </div>
        </div>

        <!-- Subtab 1: Cross-Table Matrix Table -->
        <div id="cup26SubView_matrix" class="cup26-subview">
          <div class="border border-slate-200 rounded-2xl overflow-hidden shadow-xs bg-white">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse text-xs sm:text-sm">
                <thead>
                  <tr class="bg-slate-900 text-white font-bold uppercase tracking-wider text-[11px]">
                    <th class="py-3 px-3 text-center">#</th>
                    <th class="py-3 px-4">Team Name (Hover for Roster)</th>
                    <th class="py-3 px-2 text-center bg-slate-800">R1</th>
                    <th class="py-3 px-2 text-center">R2</th>
                    <th class="py-3 px-2 text-center bg-slate-800">R3</th>
                    <th class="py-3 px-2 text-center">R4</th>
                    <th class="py-3 px-2 text-center bg-slate-800">R5</th>
                    <th class="py-3 px-2 text-center">R6</th>
                    <th class="py-3 px-2 text-center bg-slate-800">R7</th>
                    <th class="py-3 px-2 text-center">Pen</th>
                    <th class="py-3 px-3 text-right">Total IMP</th>
                    <th class="py-3 px-4 text-right bg-emerald-900 text-amber-300 font-black">Total V.P</th>
                  </tr>
                </thead>
                <tbody id="cup26MatrixBody" class="divide-y divide-slate-200 bg-white">
                  <!-- Dynamically populated with hover popovers -->
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Subtab 2: Match-by-Match Schedule & Results -->
        <div id="cup26SubView_sched" class="cup26-subview hidden">
          <div id="cup26ScheduleContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            <!-- Dynamically populated with match cards & scores -->
          </div>
        </div>

        <!-- Subtab 3: Participating Clubs & Rosters Cards -->
        <div id="cup26SubView_clubs" class="cup26-subview hidden">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="jordanCupCards">
            <!-- Dynamically populated with hover roster trigger -->
          </div>
        </div>

      </div>

      <!-- TOURNAMENT 2: JORDAN CUP 2025 FINAL MATRIX -->
      <div id="view_cup25" class="sheet-view hidden">
        <div class="bg-slate-50 p-4 rounded-t-2xl border border-b-0 border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div class="flex items-center gap-2">
            <span class="font-bold text-slate-900">Jordan Cup 2025 Final:</span>
            <span class="text-slate-600">Director Raad Otoom • 14 Rounds Total</span>
          </div>
          <a href="public/archive/Jordan Cups 2025 Final.xlsx" download class="inline-flex items-center gap-1.5 font-bold text-emerald-700 hover:text-emerald-800 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-xs">
            <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5"></i>
            <span>Download Cup 2025 Excel (.xlsx)</span>
          </a>
        </div>

        <div class="border border-slate-200 rounded-b-2xl overflow-hidden shadow-xs bg-white">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr class="bg-slate-900 text-white font-bold uppercase tracking-wider text-[11px]">
                  <th class="py-3 px-3 text-center">#</th>
                  <th class="py-3 px-4">Team Name (Hover for Roster)</th>
                  <th class="py-3 px-2 text-center bg-slate-800">After R7</th>
                  <th class="py-3 px-2 text-center">R8</th>
                  <th class="py-3 px-2 text-center bg-slate-800">R9</th>
                  <th class="py-3 px-2 text-center">R10</th>
                  <th class="py-3 px-2 text-center bg-slate-800">R11</th>
                  <th class="py-3 px-2 text-center">R12</th>
                  <th class="py-3 px-2 text-center bg-slate-800">R13</th>
                  <th class="py-3 px-2 text-center">R14</th>
                  <th class="py-3 px-4 text-right bg-emerald-900 text-amber-300 font-black">Total V.P</th>
                </tr>
              </thead>
              <tbody id="cup25MatrixBody" class="divide-y divide-slate-200 bg-white">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TOURNAMENT 3: MIXED SELECTION 2025 LEADERBOARD -->
      <div id="view_mix25" class="sheet-view hidden">
        <div class="bg-slate-50 p-4 rounded-t-2xl border border-b-0 border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div class="flex items-center gap-2">
            <span class="font-bold text-slate-900">National Mixed Pairs Selection 2025:</span>
            <span class="text-slate-600">Official IMPs & Victory Points</span>
          </div>
          <a href="public/archive/MIX SELECTION FINAL.xlsx" download class="inline-flex items-center gap-1.5 font-bold text-emerald-700 hover:text-emerald-800 bg-white px-3 py-1.5 rounded-lg border border-slate-200 shadow-xs">
            <i data-lucide="file-spreadsheet" class="w-3.5 h-3.5"></i>
            <span>Download Mixed Selection (.xlsx)</span>
          </a>
        </div>

        <div class="border border-slate-200 rounded-b-2xl overflow-hidden shadow-xs bg-white">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs sm:text-sm">
              <thead>
                <tr class="bg-slate-900 text-white font-bold uppercase tracking-wider text-[11px]">
                  <th class="py-3 px-3 text-center">#</th>
                  <th class="py-3 px-4">Pairs Name</th>
                  <th class="py-3 px-3 text-center bg-slate-800">R1 (IMP / VP)</th>
                  <th class="py-3 px-3 text-center">R2 (IMP / VP)</th>
                  <th class="py-3 px-3 text-center bg-slate-800">R3 (IMP / VP)</th>
                  <th class="py-3 px-3 text-center">R4 (IMP / VP)</th>
                  <th class="py-3 px-3 text-center bg-slate-800">R5 (IMP / VP)</th>
                  <th class="py-3 px-3 text-right">Total IMP</th>
                  <th class="py-3 px-4 text-right bg-emerald-900 text-amber-300 font-black">Total V.P</th>
                </tr>
              </thead>
              <tbody id="mix25TableBody" class="divide-y divide-slate-200 bg-white">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- SECTION 4: HISTORICAL TOURNAMENT PHOTO GALLERY (WITH LIGHTBOX ZOOM) -->
  <section id="gallery" class="py-16 bg-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-2xl mx-auto mb-12">
        <span class="text-xs font-bold uppercase tracking-wider text-sky-800 bg-sky-100 px-3 py-1 rounded-full inline-block mb-2" data-en="Federation Archives" data-ar="أرشيف الاتحاد المصور">Federation Archives</span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="Photo Gallery & Champions Hall" data-ar="معرض الصور وسجل الأبطال">Photo Gallery & Champions Hall</h2>
        <p class="text-sm text-slate-600 mt-2" data-en="Memorable moments from the Jordan International Bridge Festivals, BFAME Championships in Chennai, and podium ceremonies. Click any photo to view in high resolution." data-ar="لحظات تاريخية خالدة من مهرجانات الأردن الدولية، بطولات آسيا والشرق الأوسط (BFAME)، ومنصات التتويج. انقر على أي صورة لمشاهدتها بالحجم الكامل.">
          Memorable moments from the Jordan International Bridge Festivals, BFAME Championships in Chennai, and podium ceremonies. Click any photo to view in high resolution.
        </p>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4" id="galleryGrid">
        <!-- Dynamically populated from 21 gallery images with lightbox click -->
      </div>

    </div>
  </section>

  <!-- SECTION 5: EXECUTIVE COMMITTEE & GENERAL ASSEMBLY -->
  <section id="committee" class="py-16 bg-slate-50 border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-2xl mx-auto mb-12">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-600 bg-slate-200 px-3 py-1 rounded-full inline-block mb-2" data-en="Federation Leadership" data-ar="قيادة وإدارة الاتحاد">Federation Leadership</span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="Executive Board & General Assembly" data-ar="مجلس الإدارة والهيئة العامة">Executive Board & General Assembly</h2>
        <p class="text-sm text-slate-600 mt-2" data-en="Duly elected members and officers overseeing the development of bridge across Jordan." data-ar="أعضاء مجلس الإدارة والهيئة العامة المنتخبون والمعتمدون لدى اللجنة الأولمبية الأردنية.">
          Duly elected members and officers overseeing the development of bridge across Jordan.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5" id="committeeGrid">
        <!-- Dynamically populated from committee.json -->
      </div>

    </div>
  </section>

  <!-- SECTION 6: COMPLETE DOCUMENT ARCHIVE & REGULATIONS (14 OFFICIAL DOCUMENTS) -->
  <section id="documents" class="py-16 bg-white border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="text-center max-w-2xl mx-auto mb-10">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-600 bg-slate-200 px-3 py-1 rounded-full inline-block mb-2" data-en="Governance & Regulations" data-ar="الأنظمة واللوائح والقرارات">Governance & Regulations</span>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900" data-en="Complete Federation Document Archive" data-ar="أرشيف الوثائق واللوائح الرسمية الكامل">Complete Federation Document Archive</h2>
        <p class="text-sm text-slate-600 mt-2" data-en="100% of the federation bylaws, Olympic statutes, daily tournament bulletins, and international policies preserved." data-ar="جميع الأنظمة الأساسية، لوائح اللجنة الأولمبية، النشرات اليومية، والسياسات الدولية محفوظة ومتاحة للجميع.">
          100% of the federation bylaws, Olympic statutes, daily tournament bulletins, and international policies preserved.
        </p>
      </div>

      <!-- Filter Categories -->
      <div class="flex flex-wrap items-center justify-center gap-2 mb-8">
        <button onclick="filterDocuments('all')" class="doc-filter-btn active px-3.5 py-1.5 rounded-xl text-xs font-bold bg-sky-700 text-white shadow-xs">All Documents (14)</button>
        <button onclick="filterDocuments('governance')" class="doc-filter-btn px-3.5 py-1.5 rounded-xl text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200">Governance & Bylaws</button>
        <button onclick="filterDocuments('bulletins')" class="doc-filter-btn px-3.5 py-1.5 rounded-xl text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200">Festival Bulletins (1–4)</button>
        <button onclick="filterDocuments('regulations')" class="doc-filter-btn px-3.5 py-1.5 rounded-xl text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200">WBF & Regulations</button>
        <button onclick="filterDocuments('festival')" class="doc-filter-btn px-3.5 py-1.5 rounded-xl text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200">Festival Programs</button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" id="documentsGrid">
        <!-- Dynamically populated from docs_inventory -->
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

  <!-- FOOTER -->
  <footer class="bg-slate-950 text-slate-400 py-12 border-t border-slate-800 mt-auto text-xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
      
      <div class="flex items-center gap-3">
        <img src="public/jbf_logo.jpg" alt="JBF" class="h-10 w-auto rounded border border-slate-700">
        <div>
          <span class="block text-slate-200 font-bold text-sm">Jordan Bridge Federation (JBF)</span>
          <span class="text-slate-500">© 2026 Hashemite Kingdom of Jordan • JOC Affiliate. All Rights Reserved.</span>
        </div>
      </div>

      <div class="flex items-center gap-4">
        <button onclick="openAdminModal()" class="inline-flex items-center gap-1.5 text-xs text-amber-400 hover:text-amber-300 font-bold bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg">
          <i data-lucide="shield-check" class="w-4 h-4"></i>
          <span data-en="Admin Data Entry" data-ar="إدخال بيانات المشرف">Admin Data Entry</span>
        </button>
        <div class="text-center sm:text-right">
          <p class="text-slate-400">Official Web Domain: <span class="text-amber-400 font-semibold">jordanbridgefederation.com</span></p>
          <p class="text-slate-600 mt-0.5">Olympic Sports City • Prince Hamza Hall • Amman</p>
        </div>
      </div>

    </div>
  </footer>

  <!-- LIGHTBOX MODAL COMPONENT (FOR POSTERS & GALLERY) -->
  <div id="lightboxModal" class="fixed inset-0 z-50 bg-slate-950/90 backdrop-blur-md hidden items-center justify-center p-4" onclick="closeLightbox(event)">
    <div class="relative max-w-5xl max-h-[90vh] flex flex-col items-center" onclick="event.stopPropagation()">
      <button onclick="closeLightbox()" class="absolute -top-12 right-0 text-white/80 hover:text-white p-2 rounded-full bg-white/10 hover:bg-white/20 transition-colors">
        <i data-lucide="x" class="w-6 h-6"></i>
      </button>
      <img id="lightboxImage" src="" alt="Enlarged Poster / Photo" class="max-h-[82vh] w-auto object-contain rounded-xl shadow-2xl border border-white/10">
      <p id="lightboxCaption" class="mt-3 text-sm text-slate-200 font-medium text-center"></p>
    </div>
  </div>

  <!-- TEAM ROSTER & LINE-UP POPOVER (FOR DESKTOP HOVER & MOBILE TAP) -->
  <div id="rosterTooltip" class="fixed z-50 pointer-events-none hidden bg-slate-950/95 backdrop-blur-md text-white text-xs p-4 rounded-2xl shadow-2xl border border-slate-700/80 max-w-sm transition-opacity duration-150">
    <div class="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-slate-800">
      <div class="flex items-center gap-1.5 font-black text-amber-400">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="tooltipTeamName" class="text-sm">Team Name</span>
      </div>
      <span id="tooltipDelegation" class="text-[10px] text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded-full font-medium truncate max-w-[150px]">Delegation</span>
    </div>
    <div id="tooltipPlayerList" class="space-y-1">
      <!-- Injected player chips -->
    </div>
  </div>

  <!-- ADMIN DATA ENTRY MODAL (FOR JBF STAFF TO UPDATE SCORES EASILY) -->
  <div id="adminModal" class="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-xl max-h-[90vh] overflow-y-auto p-6 text-slate-800" onclick="event.stopPropagation()">
      
      <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-5">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center">
            <i data-lucide="shield-check" class="w-5 h-5"></i>
          </div>
          <div>
            <h3 class="font-black text-slate-900 text-base" data-en="JBF Score & Data Entry Portal" data-ar="بوابة إدخال وتعديل نتائج الاتحاد">JBF Score & Data Entry Portal</h3>
            <p class="text-xs text-slate-500" data-en="Easily enter tournament scores and team rosters without touching code." data-ar="إدخال نتائج البطولات وكشوفات الفرق بسهولة دون الحاجة لخبرة برمجية.">Easily enter tournament scores and team rosters.</p>
          </div>
        </div>
        <button onclick="closeAdminModal()" class="text-slate-400 hover:text-slate-600 p-1 rounded-lg">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- PIN Input -->
      <div id="adminPinSection" class="space-y-4">
        <p class="text-xs text-slate-600" data-en="Please enter the Federation Admin PIN to access data entry:" data-ar="يرجى إدخال رمز التحقق الخاص بمشرفي الاتحاد:">Please enter the Federation Admin PIN to access data entry:</p>
        <div class="flex gap-2">
          <input type="password" id="adminPinInput" placeholder="••••••••" onkeydown="if(event.key==='Enter') verifyAdminPin()" class="px-3.5 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:outline-none flex-1 font-mono">
          <button onclick="verifyAdminPin()" class="px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition-all">
            <span data-en="Unlock" data-ar="دخول">Unlock</span>
          </button>
        </div>
        <p id="adminPinError" class="text-xs text-red-600 hidden">Incorrect PIN. Please try again.</p>
      </div>

      <!-- Data Entry Form (Unlocked) -->
      <div id="adminFormSection" class="hidden space-y-4">
        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Target Tournament:</label>
          <select id="adminTargetTourney" class="w-full text-xs p-2.5 border border-slate-300 rounded-xl focus:ring-2 focus:ring-sky-500">
            <option value="jordancup2026">Jordan Cup 2026 Final</option>
            <option value="festival2026">Jordan Bridge Festival 2026</option>
          </select>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Team Name:</label>
            <input type="text" id="adminTeamName" placeholder="e.g. Al Nashama" class="w-full text-xs p-2.5 border border-slate-300 rounded-xl">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Rank (#):</label>
            <input type="number" id="adminTeamRank" placeholder="1" class="w-full text-xs p-2.5 border border-slate-300 rounded-xl">
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Total V.P Score:</label>
            <input type="number" step="0.01" id="adminTeamVp" placeholder="90.90" class="w-full text-xs p-2.5 border border-slate-300 rounded-xl">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-700 mb-1">Total IMP (Differential):</label>
            <input type="number" id="adminTeamImp" placeholder="+79" class="w-full text-xs p-2.5 border border-slate-300 rounded-xl">
          </div>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-700 mb-1">Player Roster (comma-separated):</label>
          <input type="text" id="adminTeamRoster" placeholder="Abdlah Ajlouni, Zaid Bitar, Samer Haddad" class="w-full text-xs p-2.5 border border-slate-300 rounded-xl">
          <span class="text-[11px] text-slate-400 mt-0.5 block">Separate each player's name with a comma.</span>
        </div>

        <div class="pt-3 border-t border-slate-100 flex items-center justify-between gap-3">
          <button onclick="applyAdminUpdate()" class="px-4 py-2.5 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs rounded-xl transition-all flex items-center gap-1.5 shadow-xs">
            <i data-lucide="check" class="w-4 h-4"></i>
            <span>Apply Live Preview</span>
          </button>
          <button onclick="exportAdminJson()" class="px-4 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition-all flex items-center gap-1.5">
            <i data-lucide="code" class="w-4 h-4"></i>
            <span>Export Clean JSON</span>
          </button>
        </div>

        <div id="adminJsonOutputBox" class="hidden mt-3">
          <label class="block text-xs font-bold text-slate-600 mb-1">Exported JSON (Ready to copy/save):</label>
          <textarea id="adminJsonTextarea" rows="4" readonly class="w-full font-mono text-[11px] p-2 bg-slate-900 text-emerald-400 rounded-xl border border-slate-700"></textarea>
          <button onclick="copyAdminJson()" class="mt-1 text-xs font-bold text-sky-700 hover:underline">Copy JSON to Clipboard</button>
        </div>
      </div>

    </div>
  </div>

  <!-- EMBEDDED MASTER DATA & APPLICATION SCRIPT -->
  <script>
    const teamDirectory = {team_dir_json_str};
    const masterData = {master_json_str};
    const fest2026Rounds = {fest2026_json_str}.rounds;
    const committeeData = {comm_json_str};
    const galleryList = {gallery_json_str};

    let currentLang = 'en';
    let currentFestYear = '2026';
    let currentRoundNum = 8;
    let activeDocCategory = 'all';

    // LANGUAGE TOGGLE
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

      document.querySelectorAll('[data-en]').forEach(el => {{
        const txt = el.getAttribute('data-' + currentLang);
        if (txt) {{
          el.textContent = txt;
        }}
      }});

      renderCurrentFestivalStandings();
      renderCup26Matrix();
      renderCup25Matrix();
      renderJordanCupCards();
      renderCommittee();
    }}

    // MOBILE MENU
    function toggleMobileMenu() {{
      const menu = document.getElementById('mobileMenu');
      menu.classList.toggle('hidden');
    }}

    // LIGHTBOX
    function openLightbox(src, caption) {{
      const modal = document.getElementById('lightboxModal');
      const img = document.getElementById('lightboxImage');
      const cap = document.getElementById('lightboxCaption');
      img.src = src;
      cap.textContent = caption || '';
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }}

    function closeLightbox(e) {{
      if (e && e.target && e.target.id === 'lightboxImage') return;
      const modal = document.getElementById('lightboxModal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') {{
        closeLightbox();
        closeAdminModal();
      }}
    }});

    // ROSTER & TEAM DIRECTORY POPOVER
    function showRosterTooltip(el, teamName) {{
      if (!teamName) return;
      const cleanName = teamName.replace('👥', '').trim();
      const upperName = cleanName.toUpperCase();
      const info = teamDirectory[upperName] || teamDirectory[cleanName] || {{
        delegation: 'Jordan Bridge Festival Entry',
        roster: []
      }};

      const tooltip = document.getElementById('rosterTooltip');
      const nameEl = document.getElementById('tooltipTeamName');
      const delegationEl = document.getElementById('tooltipDelegation');
      const listEl = document.getElementById('tooltipPlayerList');

      nameEl.textContent = cleanName;
      delegationEl.textContent = info.delegation || 'Official Entry';

      if (info.roster && info.roster.length > 0) {{
        listEl.innerHTML = `
          <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">${{currentLang === 'ar' ? 'تشكيلة الفريق (اللاعبون):' : 'Team Line-up / Players:'}}</div>
          <div class="flex flex-wrap gap-1.5">
            ${{info.roster.map(p => `
              <span class="inline-flex items-center gap-1 bg-slate-800 text-slate-100 text-[11px] font-medium px-2 py-0.5 rounded-md border border-slate-700">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                ${{p}}
              </span>
            `).join('')}}
          </div>
        `;
      }} else if (info.captain) {{
        listEl.innerHTML = `
          <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">${{currentLang === 'ar' ? 'الكابتن / قائد الفريق:' : 'Team Leader / Captain:'}}</div>
          <span class="inline-flex items-center gap-1 bg-slate-800 text-amber-300 text-xs font-bold px-2 py-0.5 rounded-md border border-slate-700">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
            ${{info.captain}}
          </span>
        `;
      }} else {{
        listEl.innerHTML = `
          <span class="text-[11px] text-slate-400 italic">Jordan International Bridge Festival Delegation</span>
        `;
      }}

      tooltip.classList.remove('hidden');

      // Accurate Positioning relative to element
      const rect = el.getBoundingClientRect();
      const tipWidth = tooltip.offsetWidth || 290;
      const tipHeight = tooltip.offsetHeight || 115;

      let left = rect.left + (rect.width / 2) - (tipWidth / 2);
      left = Math.max(10, Math.min(window.innerWidth - tipWidth - 10, left));

      let top = rect.top - tipHeight - 10;
      if (top < 10) {{
        top = rect.bottom + 10;
      }}

      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    }}

    function hideRosterTooltip() {{
      const tooltip = document.getElementById('rosterTooltip');
      if (tooltip) tooltip.classList.add('hidden');
    }}

    // Global Event Delegation for ALL elements with data-team
    document.addEventListener('mouseover', function(e) {{
      const el = e.target.closest('[data-team]');
      if (!el) return;
      const teamName = el.getAttribute('data-team');
      if (teamName) {{
        showRosterTooltip(el, teamName);
      }}
    }});

    document.addEventListener('mouseout', function(e) {{
      const el = e.target.closest('[data-team]');
      if (el) hideRosterTooltip();
    }});

    document.addEventListener('click', function(e) {{
      const el = e.target.closest('[data-team]');
      if (el) {{
        const teamName = el.getAttribute('data-team');
        if (teamName) {{
          showRosterTooltip(el, teamName);
        }}
      }} else if (!e.target.closest('#rosterTooltip')) {{
        hideRosterTooltip();
      }}
    }});

    // FESTIVAL YEAR SELECTOR
    function selectFestivalYear(year) {{
      currentFestYear = year;
      document.querySelectorAll('.year-btn').forEach(b => {{
        if (b.id === 'btnYear' + year) {{
          b.className = 'year-btn active px-3.5 py-1.5 rounded-xl text-xs font-bold bg-sky-700 text-white shadow-xs';
        }} else {{
          b.className = 'year-btn px-3.5 py-1.5 rounded-xl text-xs font-bold text-slate-700 hover:bg-slate-100';
        }}
      }});

      const fest = masterData.historicalFestivals[year];
      if (fest) {{
        document.getElementById('festivalDisplayTitle').textContent = fest.title;
        document.getElementById('festivalMetaInfo').textContent = `Official Scoring • Tournament Director: ${{fest.director}} • Total Teams: ${{fest.totalTeams}}`;
      }}

      // Show/hide subtabs: rounds are only available for 2026
      const subtabContainer = document.getElementById('subtabContainer');
      if (year === '2026') {{
        subtabContainer.classList.remove('hidden');
      }} else {{
        subtabContainer.classList.add('hidden');
        switchFestivalSubtab('standings');
      }}

      renderCurrentFestivalStandings();
    }}

    // FESTIVAL SUBTAB (STANDINGS VS ROUND MATCHES)
    function switchFestivalSubtab(tab) {{
      const standingsContent = document.getElementById('tabStandingsContent');
      const roundsContent = document.getElementById('tabRoundsContent');
      const btnStandings = document.getElementById('btnTabStandings');
      const btnRounds = document.getElementById('btnTabRounds');

      if (tab === 'standings') {{
        standingsContent.classList.remove('hidden');
        roundsContent.classList.add('hidden');
        btnStandings.className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-sky-700 text-white shadow-xs transition-all';
        btnRounds.className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-white text-slate-700 hover:bg-slate-50 transition-all';
      }} else {{
        standingsContent.classList.add('hidden');
        roundsContent.classList.remove('hidden');
        btnRounds.className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-sky-700 text-white shadow-xs transition-all';
        btnStandings.className = 'px-5 py-2.5 rounded-xl font-bold text-sm bg-white text-slate-700 hover:bg-slate-50 transition-all';
        renderRoundMatches(currentRoundNum);
      }}
    }}

    // RENDER FESTIVAL STANDINGS TABLE
    function renderCurrentFestivalStandings(customList) {{
      const fest = masterData.historicalFestivals[currentFestYear];
      const list = customList || (fest ? fest.standings : []);
      const tbody = document.getElementById('standingsTableBody');
      tbody.innerHTML = '';

      list.forEach((team) => {{
        let rankBadgeClass = 'bg-slate-100 text-slate-700';
        if (team.rank === 1) rankBadgeClass = 'badge-rank-1 font-black';
        else if (team.rank === 2) rankBadgeClass = 'badge-rank-2 font-black';
        else if (team.rank === 3) rankBadgeClass = 'badge-rank-3 font-black';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-sky-50/60 transition-colors border-b border-slate-100';
        tr.innerHTML = `
          <td class="py-3 px-4 text-center">
            <span class="inline-flex items-center justify-center w-7 h-7 rounded-full text-xs ${{rankBadgeClass}}">
              ${{team.rank}}
            </span>
          </td>
          <td class="py-3 px-4 font-bold text-slate-900 cursor-pointer hover:text-sky-700 transition-colors" data-team="${{team.name}}">
            <div class="flex items-center gap-1.5">
              <span>${{team.name}}</span>
              <span class="text-[11px] text-slate-400 font-normal">👥</span>
            </div>
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

    // FILTER FESTIVAL TEAMS
    function filterFestivalTeams() {{
      const q = document.getElementById('teamSearchInput').value.toLowerCase().trim();
      const fest = masterData.historicalFestivals[currentFestYear];
      if (!fest) return;
      const filtered = fest.standings.filter(t => 
        t.name.toLowerCase().includes(q) || t.score.toString().includes(q)
      );
      renderCurrentFestivalStandings(filtered);
    }}

    // RENDER ROUND MATCHES (2026)
    function renderRoundMatches(roundNum) {{
      currentRoundNum = roundNum;
      document.querySelectorAll('.round-pill-btn').forEach(btn => {{
        if (parseInt(btn.getAttribute('data-round')) === roundNum) {{
          btn.className = 'round-pill-btn active px-4 py-2 rounded-xl text-xs font-bold bg-sky-700 text-white shadow-xs';
        }} else {{
          btn.className = 'round-pill-btn px-4 py-2 rounded-xl text-xs font-bold bg-white text-slate-700 border border-slate-300';
        }}
      }});

      const container = document.getElementById('roundMatchesContainer');
      container.innerHTML = '';
      const matches = fest2026Rounds[roundNum] || [];

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
              <span class="truncate cursor-pointer hover:text-amber-600 font-bold transition-colors flex items-center gap-1 group" data-team="${{m.homeTeam.name}}">
                <span>${{m.homeTeam.name}}</span>
                <span class="text-[10px] text-slate-400 group-hover:text-amber-600">👥</span>
              </span>
              <span class="px-2 py-0.5 rounded font-mono ${{homeWon ? 'bg-emerald-100 text-emerald-800 font-bold' : 'bg-slate-100 text-slate-600'}}">${{m.homeTeam.vp.toFixed(2)}}</span>
            </div>
            <div class="flex items-center justify-between ${{awayWon ? 'font-black text-slate-950' : 'text-slate-600'}}">
              <span class="truncate cursor-pointer hover:text-amber-600 font-bold transition-colors flex items-center gap-1 group" data-team="${{m.awayTeam.name}}">
                <span>${{m.awayTeam.name}}</span>
                <span class="text-[10px] text-slate-400 group-hover:text-amber-600">👥</span>
              </span>
              <span class="px-2 py-0.5 rounded font-mono ${{awayWon ? 'bg-emerald-100 text-emerald-800 font-bold' : 'bg-slate-100 text-slate-600'}}">${{m.awayTeam.vp.toFixed(2)}}</span>
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // SPREADSHEET TABS SWITCHER (ONE TAB PER TOURNAMENT)
    function switchSpreadsheet(sheetId) {{
      document.querySelectorAll('.sheet-tab-btn').forEach(btn => {{
        if (btn.id === 'tabBtn_' + sheetId) {{
          btn.className = 'sheet-tab-btn active px-5 py-2.5 rounded-xl font-bold text-xs sm:text-sm bg-emerald-700 text-white shadow-xs transition-all flex items-center gap-2';
        }} else {{
          btn.className = 'sheet-tab-btn px-5 py-2.5 rounded-xl font-bold text-xs sm:text-sm bg-slate-100 text-slate-700 hover:bg-slate-200 transition-all flex items-center gap-2';
        }}
      }});

      document.querySelectorAll('.sheet-view').forEach(v => v.classList.add('hidden'));
      const activeView = document.getElementById('view_' + sheetId);
      if (activeView) activeView.classList.remove('hidden');
    }}

    // SUBTAB SWITCHER FOR JORDAN CUP 2026 (MATRIX, SCORES, CLUBS)
    function switchCup26Subtab(subtab) {{
      document.querySelectorAll('.cup26-subtab').forEach(btn => {{
        if (btn.id === 'cup26SubBtn_' + subtab) {{
          btn.className = 'cup26-subtab active px-3.5 py-1.5 rounded-lg text-xs font-bold bg-emerald-700 text-white shadow-xs transition-all flex items-center gap-1.5';
        }} else {{
          btn.className = 'cup26-subtab px-3.5 py-1.5 rounded-lg text-xs font-bold bg-white text-slate-700 border border-slate-200 hover:bg-slate-100 transition-all flex items-center gap-1.5';
        }}
      }});

      document.querySelectorAll('.cup26-subview').forEach(v => v.classList.add('hidden'));
      const active = document.getElementById('cup26SubView_' + subtab);
      if (active) active.classList.remove('hidden');
    }}

    // RENDER JORDAN CUP 2026 MATRIX TABLE (WITH ROSTER HOVER)
    function renderCup26Matrix() {{
      const tbody = document.getElementById('cup26MatrixBody');
      tbody.innerHTML = '';
      const matrix = masterData.jordanCup2026.matrix;

      matrix.forEach((t) => {{
        let rankBadge = 'bg-slate-100 text-slate-700';
        if (t.rank === 1) rankBadge = 'badge-rank-1 font-black';
        else if (t.rank === 2) rankBadge = 'badge-rank-2 font-black';
        else if (t.rank === 3) rankBadge = 'badge-rank-3 font-black';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-emerald-50/50 transition-colors border-b border-slate-100';

        const rosterAttr = encodeURIComponent(JSON.stringify(t.roster || []));

        let roundsHtml = '';
        t.rounds.forEach(rnd => {{
          const isHigh = rnd.vp >= 13;
          const isLow = rnd.vp <= 7;
          const colorClass = isHigh ? 'text-emerald-700 font-bold' : (isLow ? 'text-rose-600' : 'text-slate-700');
          roundsHtml += `
            <td class="py-2.5 px-2 text-center font-mono">
              <span class="block ${{colorClass}}">${{rnd.vp.toFixed(2)}}</span>
              <span class="block text-[10px] text-slate-400 font-normal">${{rnd.imp > 0 ? '+' : ''}}${{rnd.imp}}</span>
            </td>
          `;
        }});

        tr.innerHTML = `
          <td class="py-2.5 px-3 text-center">
            <span class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs ${{rankBadge}}">
              ${{t.rank}}
            </span>
          </td>
          <td class="py-2.5 px-4 font-bold text-slate-900 cursor-pointer hover:text-emerald-700 transition-colors" data-team="${{t.team}}">
            <div class="flex items-center gap-1.5">
              <span>${{t.team}}</span>
              <i data-lucide="users" class="w-3.5 h-3.5 text-emerald-600 inline"></i>
            </div>
          </td>
          ${{roundsHtml}}
          <td class="py-2.5 px-2 text-center text-slate-400 font-mono text-xs">${{t.penalty || '0'}}</td>
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-600">${{t.totalImp > 0 ? '+' : ''}}${{t.totalImp}}</td>
          <td class="py-2.5 px-4 text-right font-mono font-extrabold text-emerald-800 text-sm bg-emerald-50">${{t.totalVp.toFixed(2)}}</td>
        `;
        tbody.appendChild(tr);
      }});
      lucide.createIcons();
    }}

    // RENDER JORDAN CUP 2026 SCHEDULE
    function renderCup26Schedule() {{
      const container = document.getElementById('cup26ScheduleContainer');
      container.innerHTML = '';
      const sched = masterData.jordanCup2026.schedule;

      sched.forEach(rnd => {{
        const card = document.createElement('div');
        card.className = 'bg-white p-4 sm:p-5 rounded-2xl border border-slate-200/90 shadow-xs flex flex-col justify-between';
        
        const matchesHtml = rnd.matches.map(m => {{
          const homeWon = m.homeVp > m.awayVp;
          const awayWon = m.awayVp > m.homeVp;
          const isDraw = m.homeVp === m.awayVp;
          const absDiff = Math.abs(m.homeImp);

          return `
            <div class="p-3 rounded-xl bg-slate-50/80 border border-slate-200/70 hover:border-emerald-300 hover:bg-emerald-50/20 transition-all">
              <div class="flex items-center justify-between gap-2">
                <!-- Home Team -->
                <div class="flex items-center gap-1.5 flex-1 min-w-0">
                  <span class="text-xs font-bold truncate cursor-pointer hover:text-emerald-700 transition-colors ${{homeWon ? 'text-slate-900 font-extrabold' : 'text-slate-600'}}" data-team="${{m.home}}">
                    ${{m.home}}
                  </span>
                  <span class="text-[11px] text-slate-400 cursor-pointer hover:text-emerald-600 transition-colors shrink-0" data-team="${{m.home}}" title="View roster">👥</span>
                </div>

                <!-- Match Score Badge (V.P.) -->
                <div class="shrink-0 flex items-center gap-1 px-2.5 py-1 rounded-lg bg-white border border-slate-200 shadow-2xs font-mono">
                  <span class="font-extrabold text-xs ${{homeWon ? 'text-emerald-700' : (isDraw ? 'text-slate-700' : 'text-slate-400')}}">${{m.homeVp.toFixed(2)}}</span>
                  <span class="text-[11px] text-slate-300 font-bold">:</span>
                  <span class="font-extrabold text-xs ${{awayWon ? 'text-emerald-700' : (isDraw ? 'text-slate-700' : 'text-slate-400')}}">${{m.awayVp.toFixed(2)}}</span>
                </div>

                <!-- Away Team -->
                <div class="flex items-center justify-end gap-1.5 flex-1 min-w-0 text-right">
                  <span class="text-[11px] text-slate-400 cursor-pointer hover:text-emerald-600 transition-colors shrink-0" data-team="${{m.away}}" title="View roster">👥</span>
                  <span class="text-xs font-bold truncate cursor-pointer hover:text-emerald-700 transition-colors ${{awayWon ? 'text-slate-900 font-extrabold' : 'text-slate-600'}}" data-team="${{m.away}}">
                    ${{m.away}}
                  </span>
                </div>
              </div>

              <!-- IMP Difference & Outcome Row -->
              <div class="flex items-center justify-between text-[11px] pt-2 mt-2 border-t border-slate-200/50 font-mono">
                <span class="${{m.homeImp > 0 ? 'text-emerald-600 font-bold' : 'text-slate-400'}}">
                  ${{m.homeImp > 0 ? '+' + m.homeImp : m.homeImp}} IMP
                </span>
                <span class="text-[10px] font-sans font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${{isDraw ? 'bg-amber-100/70 text-amber-800 border border-amber-200' : 'bg-emerald-100/70 text-emerald-800 border border-emerald-200'}}">
                  ${{isDraw ? 'Tie (Draw)' : (homeWon ? `${{m.home}} Win (+${{absDiff}})` : `${{m.away}} Win (+${{absDiff}})` )}}
                </span>
                <span class="${{m.awayImp > 0 ? 'text-emerald-600 font-bold' : 'text-slate-400'}}">
                  ${{m.awayImp > 0 ? '+' + m.awayImp : m.awayImp}} IMP
                </span>
              </div>
            </div>
          `;
        }}).join('');

        card.innerHTML = `
          <div class="flex items-center justify-between pb-2.5 mb-3 border-b border-slate-100">
            <span class="text-xs font-black text-emerald-800 uppercase tracking-wider flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-600"></span>
              Round #${{rnd.round}}
            </span>
            <span class="text-[11px] font-medium text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">Jordan Cup 2026</span>
          </div>
          <div class="space-y-2.5">
            ${{matchesHtml}}
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // RENDER JORDAN CUP 2025 MATRIX
    function renderCup25Matrix() {{
      const tbody = document.getElementById('cup25MatrixBody');
      tbody.innerHTML = '';
      const matrix = masterData.jordanCup2025.matrix;

      matrix.forEach((t) => {{
        let rankBadge = 'bg-slate-100 text-slate-700';
        if (t.rank === 1) rankBadge = 'badge-rank-1 font-black';
        else if (t.rank === 2) rankBadge = 'badge-rank-2 font-black';
        else if (t.rank === 3) rankBadge = 'badge-rank-3 font-black';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-emerald-50/50 transition-colors border-b border-slate-100';

        let roundsHtml = '';
        t.rounds.forEach(r => {{
          roundsHtml += `<td class="py-2 px-2 text-center font-mono text-slate-700">${{r.vp > 0 ? r.vp.toFixed(2) : '-'}}</td>`;
        }});

        tr.innerHTML = `
          <td class="py-2.5 px-3 text-center">
            <span class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs ${{rankBadge}}">
              ${{t.rank}}
            </span>
          </td>
          <td class="py-2.5 px-4 font-bold text-slate-900 cursor-pointer hover:text-emerald-700 transition-colors" data-team="${{t.team}}">
            <div class="flex items-center gap-1.5">
              <span>${{t.team}}</span>
              <i data-lucide="users" class="w-3.5 h-3.5 text-emerald-600 inline"></i>
            </div>
          </td>
          ${{roundsHtml}}
          <td class="py-2.5 px-4 text-right font-mono font-extrabold text-emerald-800 text-sm bg-emerald-50">${{t.totalVp.toFixed(2)}}</td>
        `;
        tbody.appendChild(tr);
      }});
      lucide.createIcons();
    }}

    // RENDER MIXED SELECTION 2025
    function renderMix25() {{
      const tbody = document.getElementById('mix25TableBody');
      tbody.innerHTML = '';
      const pairs = masterData.mixSelection2025.pairs;

      pairs.forEach(p => {{
        let rankBadge = 'bg-slate-100 text-slate-700';
        if (p.rank === 1) rankBadge = 'badge-rank-1 font-black';
        else if (p.rank === 2) rankBadge = 'badge-rank-2 font-black';
        else if (p.rank === 3) rankBadge = 'badge-rank-3 font-black';

        const tr = document.createElement('tr');
        tr.className = 'hover:bg-indigo-50/40 transition-colors border-b border-slate-100';

        let rndHtml = '';
        p.rounds.forEach(r => {{
          rndHtml += `
            <td class="py-2 px-3 text-center font-mono text-xs">
              <span class="font-bold text-indigo-950">${{r.vp.toFixed(2)}}</span>
              <span class="text-[10px] text-slate-400 block">${{r.imp > 0 ? '+' : ''}}${{r.imp}} IMP</span>
            </td>
          `;
        }});

        tr.innerHTML = `
          <td class="py-2.5 px-3 text-center">
            <span class="inline-flex items-center justify-center w-6 h-6 rounded-full text-xs ${{rankBadge}}">
              ${{p.rank}}
            </span>
          </td>
          <td class="py-2.5 px-4 font-bold text-slate-900">${{p.pair}}</td>
          ${{rndHtml}}
          <td class="py-2.5 px-3 text-right font-mono font-bold text-slate-600">${{p.totalImp > 0 ? '+' : ''}}${{p.totalImp}}</td>
          <td class="py-2.5 px-4 text-right font-mono font-extrabold text-indigo-900 text-sm bg-indigo-50">${{p.totalVp.toFixed(2)}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // RENDER JORDAN CUP CARDS (CLEAN HOVER TRIGGER, NO OPEN ROSTER CLUTTER)
    function renderJordanCupCards() {{
      const container = document.getElementById('jordanCupCards');
      container.innerHTML = '';
      const matrix = masterData.jordanCup2026.matrix;

      matrix.forEach(t => {{
        const card = document.createElement('div');
        card.className = 'bg-white p-5 rounded-2xl border border-slate-200 hover:border-emerald-400 hover:shadow-md transition-all flex flex-col justify-between group';
        
        let rankColor = 'bg-slate-200 text-slate-800';
        if (t.rank === 1) rankColor = 'badge-rank-1 font-black';
        else if (t.rank === 2) rankColor = 'badge-rank-2 font-black';
        else if (t.rank === 3) rankColor = 'badge-rank-3 font-black';

        const pCount = (t.roster && t.roster.length) ? t.roster.length : 6;
        const triggerHtml = `
          <div class="mt-3 pt-3 border-t border-slate-100">
            <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-50 hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 border border-slate-200/90 hover:border-emerald-300 text-xs font-semibold cursor-pointer transition-all shadow-2xs group-hover:border-emerald-300" data-team="${{t.team}}">
              <span class="text-xs">👥</span>
              <span>${{pCount}} ${{currentLang === 'ar' ? 'لاعبين • مرر لرؤية التشكيلة' : 'Players • Hover for Roster'}}</span>
            </div>
          </div>
        `;

        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold ${{rankColor}} shadow-xs">#${{t.rank}}</span>
              <span class="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full ${{t.totalImp >= 0 ? 'bg-emerald-50 text-emerald-800 border border-emerald-200/60' : 'bg-slate-100 text-slate-600'}}">
                ${{t.totalImp > 0 ? '+' : ''}}${{t.totalImp}} IMP
              </span>
            </div>
            <h4 class="font-black text-slate-900 text-lg mb-1 cursor-pointer hover:text-emerald-700 transition-colors flex items-center gap-1.5" data-team="${{t.team}}">
              <span>${{t.team}}</span>
              <span class="text-xs text-slate-400">👥</span>
            </h4>
            <span class="text-xs text-slate-500 block">${{currentLang === 'ar' ? 'الدوري الرسمي لكأس الأردن' : 'Official Jordan Cup League'}}</span>
            ${{triggerHtml}}
          </div>

          <div class="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between">
            <span class="text-xs font-semibold text-slate-500">${{currentLang === 'ar' ? 'مجموع النقاط:' : 'Total V.P:'}}</span>
            <span class="text-xl font-black font-mono text-emerald-800">${{t.totalVp.toFixed(2)}}</span>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // RENDER GALLERY WITH LIGHTBOX ZOOM
    function renderGallery() {{
      const container = document.getElementById('galleryGrid');
      container.innerHTML = '';

      galleryList.forEach(imgName => {{
        const card = document.createElement('div');
        card.className = 'group relative rounded-xl overflow-hidden border border-slate-200 shadow-xs hover:shadow-md transition-all cursor-pointer bg-slate-900 aspect-4/3';
        const imgPath = 'public/gallery/' + imgName;
        const caption = imgName.replace(/_/g, ' ').replace('.jpg', '').replace('.png', '');

        card.onclick = () => openLightbox(imgPath, 'JBF Tournament History: ' + caption);
        card.innerHTML = `
          <img src="${{imgPath}}" alt="${{caption}}" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300">
          <div class="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white">
            <i data-lucide="zoom-in" class="w-6 h-6"></i>
          </div>
        `;
        container.appendChild(card);
      }});
      lucide.createIcons();
    }}

    // RENDER COMMITTEE (OFFICIAL EXECUTIVE BOARD WITH BRIDGWEBS PHOTOS)
    function renderCommittee() {{
      const container = document.getElementById('committeeGrid');
      container.innerHTML = '';

      committeeData.members.forEach(m => {{
        const card = document.createElement('div');
        card.className = 'bg-white p-5 rounded-2xl border border-slate-200 text-sm hover:border-amber-400 hover:shadow-md transition-all flex flex-col sm:flex-row items-center sm:items-start gap-4 text-center sm:text-left';
        
        const displayName = currentLang === 'ar' ? (m.name_ar || m.name) : m.name;
        const displayRole = currentLang === 'ar' ? (m.role_ar || m.role) : m.role;

        const avatarHtml = m.photo ? 
          `<div class="relative group cursor-pointer shrink-0" onclick="openLightbox('${{m.photo}}', '${{displayName}} - ${{displayRole}}')">
             <img src="${{m.photo}}" alt="${{displayName}}" class="w-20 h-24 object-cover rounded-xl border-2 border-slate-200 group-hover:border-amber-400 shadow-sm transition-all">
             <div class="absolute inset-0 bg-slate-900/30 opacity-0 group-hover:opacity-100 rounded-xl transition-opacity flex items-center justify-center text-white text-xs">
               <i data-lucide="zoom-in" class="w-4 h-4"></i>
             </div>
           </div>` :
          `<div class="w-20 h-24 rounded-xl bg-sky-100 text-sky-800 font-bold flex items-center justify-center text-xs shrink-0 border border-sky-200">
             <i data-lucide="user" class="w-6 h-6"></i>
           </div>`;

        card.innerHTML = `
          ${{avatarHtml}}
          <div class="min-w-0 flex-1 flex flex-col justify-between h-full">
            <div>
              <span class="inline-block text-[11px] font-bold text-amber-700 bg-amber-50 border border-amber-200 px-2.5 py-0.5 rounded-full mb-1">${{displayRole}}</span>
              <strong class="block text-slate-900 font-black text-base truncate">${{displayName}}</strong>
            </div>
            <div class="mt-3 pt-2 border-t border-slate-100 text-xs space-y-0.5">
              ${{m.phone ? `<span class="block font-mono text-slate-500 text-[11px]" dir="ltr">📞 ${{m.phone}}</span>` : ''}}
              ${{m.email ? `<span class="block text-slate-400 text-[11px] truncate">✉️ ${{m.email}}</span>` : ''}}
            </div>
          </div>
        `;
        container.appendChild(card);
      }});
      lucide.createIcons();
    }}

    // RENDER DOCUMENTS ARCHIVE
    function filterDocuments(category) {{
      activeDocCategory = category;
      document.querySelectorAll('.doc-filter-btn').forEach(btn => {{
        if (btn.textContent.toLowerCase().includes(category)) {{
          btn.className = 'doc-filter-btn active px-3.5 py-1.5 rounded-xl text-xs font-bold bg-sky-700 text-white shadow-xs';
        }} else {{
          btn.className = 'doc-filter-btn px-3.5 py-1.5 rounded-xl text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200';
        }}
      }});
      renderDocuments();
    }}

    function renderDocuments() {{
      const container = document.getElementById('documentsGrid');
      container.innerHTML = '';

      const docs = masterData.documents.filter(d => activeDocCategory === 'all' || d.category === activeDocCategory);

      docs.forEach(d => {{
        const card = document.createElement('div');
        card.className = 'bg-white p-5 rounded-2xl border border-slate-200 shadow-xs hover:border-sky-400 hover:shadow-md transition-all flex flex-col justify-between';
        
        const isPdf = d.filetype === 'PDF';
        const actionLabel = isPdf ? (currentLang === 'ar' ? 'عرض الوثيقة (PDF)' : 'View Document (PDF)') : (currentLang === 'ar' ? 'تحميل الملف' : 'Download File');
        const iconName = d.icon || 'file-text';
        const fileUrl = 'public/archive/' + d.filename;

        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between mb-3">
              <div class="w-9 h-9 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center">
                <i data-lucide="${{iconName}}" class="w-4 h-4"></i>
              </div>
              <span class="text-[11px] font-bold text-slate-400 font-mono">${{d.filesize}} • ${{d.filetype}}</span>
            </div>
            <h3 class="font-bold text-slate-900 text-sm mb-1">${{currentLang === 'ar' ? d.title_ar : d.title_en}}</h3>
            <p class="text-xs text-slate-500 mb-4 leading-relaxed">${{currentLang === 'ar' ? d.desc_ar : d.desc_en}}</p>
          </div>
          <a href="${{fileUrl}}" target="_blank" ${{isPdf ? '' : 'download'}} class="inline-flex items-center justify-between text-xs font-bold text-sky-700 hover:text-sky-800 bg-sky-50 hover:bg-sky-100 px-3.5 py-2 rounded-xl transition-all">
            <span>${{actionLabel}}</span>
            <i data-lucide="${{isPdf ? 'arrow-right' : 'download'}}" class="w-3.5 h-3.5"></i>
          </a>
        `;
        container.appendChild(card);
      }});
      lucide.createIcons();
    }}

    // ADMIN DATA ENTRY MODAL
    function openAdminModal() {{
      const modal = document.getElementById('adminModal');
      const pinInput = document.getElementById('adminPinInput');
      if (pinInput) pinInput.value = '';
      const err = document.getElementById('adminPinError');
      if (err) err.classList.add('hidden');
      modal.classList.remove('hidden');
      modal.classList.add('flex');
      if (pinInput) setTimeout(() => pinInput.focus(), 100);
    }}

    function closeAdminModal() {{
      const modal = document.getElementById('adminModal');
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }}

    async function verifyAdminPin() {{
      const pin = document.getElementById('adminPinInput').value;
      const err = document.getElementById('adminPinError');
      // Secure SHA-256 cryptographic verification — password is never exposed in plain text
      const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(pin));
      const hash = Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
      if (hash === 'f54dfd493397bd939a0f3a00d0a8a47b5e72022cc7d55851dac58e1a8b1de00f') {{
        document.getElementById('adminPinSection').classList.add('hidden');
        document.getElementById('adminFormSection').classList.remove('hidden');
        err.classList.add('hidden');
      }} else {{
        err.classList.remove('hidden');
      }}
    }}

    function applyAdminUpdate() {{
      const tName = document.getElementById('adminTeamName').value.trim();
      const rank = parseInt(document.getElementById('adminTeamRank').value);
      const vp = parseFloat(document.getElementById('adminTeamVp').value);
      const imp = parseInt(document.getElementById('adminTeamImp').value) || 0;
      const rosterRaw = document.getElementById('adminTeamRoster').value.trim();
      const roster = rosterRaw ? rosterRaw.split(',').map(s => s.trim()).filter(Boolean) : [];

      if (!tName || isNaN(vp)) {{
        alert('Please provide at least a Team Name and Total V.P score.');
        return;
      }}

      // Find or add in Jordan Cup matrix
      let existing = masterData.jordanCup2026.matrix.find(x => x.team.toLowerCase() === tName.toLowerCase());
      if (existing) {{
        existing.totalVp = vp;
        existing.totalImp = imp;
        if (!isNaN(rank)) existing.rank = rank;
        if (roster.length > 0) existing.roster = roster;
      }} else {{
        masterData.jordanCup2026.matrix.push({{
          team: tName,
          rank: rank || masterData.jordanCup2026.matrix.length + 1,
          totalVp: vp,
          totalImp: imp,
          rounds: [],
          penalty: 0,
          roster: roster
        }});
      }}

      // Re-sort and re-render
      masterData.jordanCup2026.matrix.sort((a, b) => b.totalVp - a.totalVp);
      renderCup26Matrix();
      renderJordanCupCards();
      alert('Live update applied! Check the tables and cards below.');
    }}

    function exportAdminJson() {{
      const box = document.getElementById('adminJsonOutputBox');
      const textarea = document.getElementById('adminJsonTextarea');
      box.classList.remove('hidden');
      textarea.value = JSON.stringify(masterData.jordanCup2026.matrix, null, 2);
    }}

    function copyAdminJson() {{
      const textarea = document.getElementById('adminJsonTextarea');
      textarea.select();
      document.execCommand('copy');
      alert('JSON copied to clipboard!');
    }}

    // INITIALIZATION
    window.addEventListener('DOMContentLoaded', () => {{
      lucide.createIcons();
      selectFestivalYear('2026');
      renderCup26Matrix();
      renderCup26Schedule();
      renderCup25Matrix();
      renderMix25();
      renderJordanCupCards();
      renderGallery();
      renderCommittee();
      renderDocuments();
    }});
  </script>
</body>
</html>'''

with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"SUCCESS: Upgraded build_site.py and written index.html ({len(html_content)} bytes)")
