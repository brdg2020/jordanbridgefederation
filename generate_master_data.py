import os
import json
import re
import openpyxl

base_dir = os.path.dirname(os.path.abspath(__file__))
archive_dir = os.path.join(base_dir, 'public/archive')
data_dir = os.path.join(base_dir, 'public/data')
os.makedirs(data_dir, exist_ok=True)

# 1. Parse Historical Festivals (2026, 2025, 2024, 2023)
festivals = {}
fest_configs = [
    ('2026', 'jordanbridgefestival2026-teams.htm', '42nd Jordan Bridge Festival (2026) - Open Teams', 'Waleed El Menyawi'),
    ('2025', 'openteams2025.htm', '41st Jordan Bridge Festival (2025) - Open Teams', 'Waleed El Menyawi'),
    ('2024', 'jordan2024-openteams.htm', '40th Jordan Bridge Festival (2024) - Open Teams', 'Waleed El Menyawi'),
    ('2023', 'jordanbridgefestival2023-teams.htm', '39th Jordan Bridge Festival (2023) - Open Teams', 'Waleed El Menyawi')
]

for year, fname, title, director in fest_configs:
    fpath = os.path.join(archive_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    pre_match = re.search(r'<PRE>(.*?)(?:<a name=\'scoretables\'|--+)', content, re.DOTALL | re.IGNORECASE)
    standings = []
    if pre_match:
        text = pre_match.group(1)
        lines = text.strip().split('\n')
        for line in lines:
            m = re.match(r'^\s*(\d+)\s+(\d+)\s+([\d\.]+)\s+(.*?)(?:\s+-[0-9\.]+)?$', line)
            if m:
                standings.append({
                    'rank': int(m.group(1)),
                    'teamId': int(m.group(2)),
                    'score': float(m.group(3)),
                    'name': m.group(4).strip()
                })
    
    festivals[year] = {
        'year': year,
        'title': title,
        'director': director,
        'totalTeams': len(standings),
        'standings': standings
    }
print(f"Parsed {len(festivals)} historical festivals.")

# 2. Parse Jordan Cup 2026 (From Jordan Cups 26 Final.xlsx & schedule)
cup2026_file = os.path.join(archive_dir, 'Jordan Cups 26 Final.xlsx')
wb_cup26 = openpyxl.load_workbook(cup2026_file, data_only=True)
ws_cup26 = wb_cup26.active

# Team rosters from Jordan Cups 26 schedule.xlsx & 26 Final
rosters_2026 = {
    'AL Nashama': ['Abdlah Ajlouni', 'Zaid Bitar', 'Samer Haddad', 'Luai Al Hussari', 'Mamoun Al Kotob', 'Omran Abu Dhaim'],
    'Lions': ['Samer Rwashdeh', 'Farah Ahmed', 'Yena Sabagh', 'Mohd Al Taji'],
    'Jordan Teams': ['Ghassan Ghaneem', 'Yasmin Abu Jaber', 'Marwan Ghaneem', 'Clement Mamar Bash', 'Rana Abdelhadi', 'Jamal Abdeljalil'],
    'Jordan Mix': ['Sakher Malkawi', 'Aaida Abu Jaber', 'Dima Al Taher', 'Ahmed Al Samhouri', 'Huda Rabaeh', 'Akiel Madi'],
    'Alfa': ['Randa Al Saket', 'Azza Qauah', 'Hala Sawaf', 'Amal Fakhouri'],
    'Eagles': ['Mona Al Omari', 'Mais Al Bitar', 'Bana Al Taher', 'Hanan Juman', 'Nowel Trawneh', 'Omar Al Masri'],
    'Ortho Group': ['Yousef Batshon', 'Jack Qarouta', 'Ramzi Qusous', 'Rageed Sabagh', 'Maya Khalaf', 'Laith Tashman'],
    'Palestine': ['Laila Zruqat', 'Hanan Al Masri', 'Nawar Hashem', 'Fiuroz Badwan', 'Alia Shredh']
}

matrix_2026 = []
for r in range(14, 22):
    tname = ws_cup26.cell(r, 1).value
    if not tname:
        continue
    tname = str(tname).strip()
    rounds = []
    # 7 rounds, each has VP and IMP
    for rnd in range(1, 8):
        c_vp = 2 + (rnd - 1) * 2
        c_imp = c_vp + 1
        vp_val = ws_cup26.cell(r, c_vp).value
        imp_val = ws_cup26.cell(r, c_imp).value
        rounds.append({
            'round': rnd,
            'vp': round(float(vp_val), 2) if vp_val is not None else 0.0,
            'imp': int(float(imp_val)) if imp_val is not None else 0
        })
    penalty = ws_cup26.cell(r, 16).value
    total_vp = ws_cup26.cell(r, 17).value
    total_imp = ws_cup26.cell(r, 18).value
    
    matrix_2026.append({
        'team': tname,
        'rounds': rounds,
        'penalty': float(penalty) if penalty is not None else 0.0,
        'totalVp': round(float(total_vp), 2) if total_vp is not None else 0.0,
        'totalImp': int(float(total_imp)) if total_imp is not None else 0,
        'roster': rosters_2026.get(tname, [])
    })

matrix_2026.sort(key=lambda x: x['totalVp'], reverse=True)
for idx, item in enumerate(matrix_2026):
    item['rank'] = idx + 1

# Schedule 2026 with Match Scores & IMPs
sched_file = os.path.join(archive_dir, 'Jordan Cups 26 schedule.xlsx')
wb_sched = openpyxl.load_workbook(sched_file, data_only=True)
ws_sched = wb_sched.active

team_aliases = {
    'lions': 'Lions',
    'eagles': 'Eagles',
    'jordan teams': 'Jordan Teams',
    'jor teams': 'Jordan Teams',
    'palestine': 'Palestine',
    'ortho group': 'Ortho Group',
    'al nashama': 'AL Nashama',
    'jordan mix': 'Jordan Mix',
    'jor mix': 'Jordan Mix',
    'alfa': 'Alfa'
}

def norm_team(name):
    clean = str(name).strip().lower()
    return team_aliases.get(clean, str(name).strip())

team_stats_map = {}
for entry in matrix_2026:
    t_name = norm_team(entry['team'])
    team_stats_map[t_name] = {}
    for r_stat in entry['rounds']:
        team_stats_map[t_name][r_stat['round']] = r_stat

raw_pairings = {
    1: [(ws_sched.cell(r, 1).value, ws_sched.cell(r, 2).value) for r in range(24, 28)],
    2: [(ws_sched.cell(r, 3).value, ws_sched.cell(r, 4).value) for r in range(24, 28)],
    3: [(ws_sched.cell(r, 1).value, ws_sched.cell(r, 2).value) for r in range(30, 34)],
    4: [(ws_sched.cell(r, 3).value, ws_sched.cell(r, 4).value) for r in range(30, 34)],
    5: [(ws_sched.cell(r, 1).value, ws_sched.cell(r, 2).value) for r in range(36, 40)],
    6: [(ws_sched.cell(r, 3).value, ws_sched.cell(r, 4).value) for r in range(36, 40)],
    7: [(ws_sched.cell(r, 1).value, ws_sched.cell(r, 2).value) for r in range(42, 46)]
}

schedule_2026 = []
for rnd in range(1, 8):
    round_matches = []
    for h_raw, a_raw in raw_pairings[rnd]:
        h = norm_team(h_raw)
        a = norm_team(a_raw)
        h_s = team_stats_map.get(h, {}).get(rnd, {'vp': 0.0, 'imp': 0})
        a_s = team_stats_map.get(a, {}).get(rnd, {'vp': 0.0, 'imp': 0})
        winner = h if h_s['vp'] > a_s['vp'] else (a if a_s['vp'] > h_s['vp'] else 'Tie')
        round_matches.append({
            'home': h,
            'away': a,
            'homeVp': h_s['vp'],
            'awayVp': a_s['vp'],
            'homeImp': h_s['imp'],
            'awayImp': a_s['imp'],
            'winner': winner
        })
    schedule_2026.append({
        'round': rnd,
        'matches': round_matches
    })

# 3. Parse Jordan Cup 2025 (Jordan Cups 2025 Final.xlsx)
cup2025_file = os.path.join(archive_dir, 'Jordan Cups 2025 Final.xlsx')
wb_cup25 = openpyxl.load_workbook(cup2025_file, data_only=True)
ws_cup25 = wb_cup25.active

# Rosters for 2025
rosters_2025 = {
    'KING HUSSEIN CLUB': ['Mamoun Al Kotob', 'Ghassan Ghaneem', 'Omran Abu Dhaim', 'Marwan Ghaneem'],
    'JBA 3': ['Farah Ahmed', 'Samer Rwashdeh', 'Dima Al Taher', 'Ahmed Al Samhouri'],
    'JBA 1': ['Mohd Al Taji', 'Yena Rageed', 'Hamzeh Habbob', 'Samer Haddad', 'Syelvi Skljean'],
    'JBA 2': ['Jamal Abdeljalil', 'Rana Abdelhadi', 'Huda Rabaia', 'Zaid Bitar'],
    'OTHODOX CLUB': ['Yousef Batshon', 'Rabeha Othman', 'Zeyad Shraehah', 'Abdlah Ajlouni', 'Farid Nabelsi', 'Jack Karouta', 'Laith Tashman'],
    'JBA 5': ['Lina Toukan', 'Maram Qusous', 'Aziz Amer', 'Nowel Trawnwh'],
    'JBA 4': ['Hanan Al Masri', 'Nawar Hashem', 'Fiuroz Badwan', 'Hala Sawaf', 'Najwa Najab', 'Hassana Zu']
}

matrix_2025 = []
for r in range(14, 21):
    tname = ws_cup25.cell(r, 1).value
    if not tname:
        continue
    tname = str(tname).strip()
    after_r7 = ws_cup25.cell(r, 2).value
    r8 = ws_cup25.cell(r, 3).value
    r9 = ws_cup25.cell(r, 4).value
    r10 = ws_cup25.cell(r, 5).value
    r11 = ws_cup25.cell(r, 6).value
    r12 = ws_cup25.cell(r, 7).value
    r13 = ws_cup25.cell(r, 8).value
    r14 = ws_cup25.cell(r, 9).value
    total_vp = ws_cup25.cell(r, 11).value
    
    rounds_vps = [
        {'label': 'After R7', 'vp': round(float(after_r7), 2) if after_r7 is not None else 0.0},
        {'label': 'R8', 'vp': round(float(r8), 2) if r8 is not None else 0.0},
        {'label': 'R9', 'vp': round(float(r9), 2) if r9 is not None else 0.0},
        {'label': 'R10', 'vp': round(float(r10), 2) if r10 is not None else 0.0},
        {'label': 'R11', 'vp': round(float(r11), 2) if r11 is not None else 0.0},
        {'label': 'R12', 'vp': round(float(r12), 2) if r12 is not None else 0.0},
        {'label': 'R13', 'vp': round(float(r13), 2) if r13 is not None else 0.0},
        {'label': 'R14', 'vp': round(float(r14), 2) if r14 is not None else 0.0}
    ]
    
    clean_total = round(float(total_vp), 2) if total_vp is not None else sum(x['vp'] for x in rounds_vps)
    matrix_2025.append({
        'team': tname,
        'rounds': rounds_vps,
        'totalVp': clean_total,
        'roster': rosters_2025.get(tname, [])
    })

matrix_2025.sort(key=lambda x: x['totalVp'], reverse=True)
for idx, item in enumerate(matrix_2025):
    item['rank'] = idx + 1

# 4. Parse Mixed Selection 2025 (MIX SELECTION FINAL.xlsx)
# The final standings are on the "BYE" sheet: 11 rounds (IMPs + VPs), totals,
# the best-9-rounds table ("Top 9 VP") and the official final ranking.
# The other sheets (Sheet1 = after 5 rounds, Sheet2/Sheet3 = after 8 rounds)
# are interim working copies of the same figures.
mix_file = os.path.join(archive_dir, 'MIX SELECTION FINAL.xlsx')
wb_mix = openpyxl.load_workbook(mix_file, data_only=True)
ws_mix = wb_mix['BYE']

def _num(v):
    return None if v is None or v == '' else float(v)

mix_by_name = {}
for r in range(14, 21):
    pname = ws_mix.cell(r, 2).value
    if not pname:
        continue
    pname = str(pname).strip()
    r_scores = []
    for rnd in range(1, 12):
        c_imp = 3 + (rnd - 1) * 2
        imp_v = _num(ws_mix.cell(r, c_imp).value)
        vp_v = _num(ws_mix.cell(r, c_imp + 1).value)
        r_scores.append({'round': rnd,
                         'imp': int(imp_v) if imp_v is not None else None,
                         'vp': round(vp_v, 2) if vp_v is not None else None})
    mix_by_name[pname] = {
        'pair': pname,
        'rounds': r_scores,
        'totalImp': int(_num(ws_mix.cell(r, 25).value)),
        'totalVp': round(_num(ws_mix.cell(r, 26).value), 2),
    }
# Top 9 VP table (rows 26-32: name in B, 9 best VPs in C..K, total in L)
for r in range(26, 33):
    pname = str(ws_mix.cell(r, 2).value).strip()
    mix_by_name[pname]['top9'] = [round(_num(ws_mix.cell(r, c).value), 2) for c in range(3, 12)]
    mix_by_name[pname]['top9Total'] = round(_num(ws_mix.cell(r, 12).value), 2)
# Final ranking (rows 38-44: name in B, Top 9 total in C, rank in D)
for r in range(38, 45):
    pname = str(ws_mix.cell(r, 2).value).strip()
    mix_by_name[pname]['rank'] = int(_num(ws_mix.cell(r, 4).value))
    assert round(_num(ws_mix.cell(r, 3).value), 2) == mix_by_name[pname]['top9Total']
mix_pairs = sorted(mix_by_name.values(), key=lambda x: x['rank'])

# 5. Documents Inventory
docs_inventory = [
    # 2026
    {
        'id': 'jordan_cup_2026_matrix',
        'category': 'tournaments',
        'title_en': 'Jordan Cup 2026 - Official Results & Score Matrix',
        'title_ar': 'كأس الأردن 2026 - النتائج الرسمية ومصفوفة النقاط',
        'desc_en': 'Complete match scores, VP standings, and IMP calculations for the 2026 premier league.',
        'desc_ar': 'نتائج المباريات الكاملة وترتيب نقاط VP وحسابات IMP لبطولة دوري كأس الأردن 2026.',
        'filename': 'Jordan Cups 26 Final.xlsx',
        'filetype': 'XLSX',
        'filesize': '97 KB',
        'date': '2026-03-01',
        'year': 2026,
        'date_display_en': 'Mar 2026',
        'date_display_ar': 'مارس 2026',
        'icon': 'table'
    },
    {
        'id': 'jordan_cup_2026_schedule',
        'category': 'tournaments',
        'title_en': 'Jordan Cup 2026 - Official Schedule & Pairings',
        'title_ar': 'كأس الأردن 2026 - جدول ومواعيد المباريات الرسمية',
        'desc_en': 'Official tournament pairings and match schedule arranged by Tournament Director Raad Otoom.',
        'desc_ar': 'جدول ومواعيد مباريات بطولة كأس الأردن الرسمية المعتمدة من مدير البطولة رعد عتوم.',
        'filename': 'Jordan Cups 26 schedule.xlsx',
        'filetype': 'XLSX',
        'filesize': '12 KB',
        'date': '2026-01-20',
        'year': 2026,
        'date_display_en': 'Jan 2026',
        'date_display_ar': 'يناير 2026',
        'icon': 'calendar'
    },
    # 2025
    {
        'id': 'wbf_women',
        'category': 'international',
        'title_en': "WBF Women's Bridge Newsletter (Onwards for the Future)",
        'title_ar': 'نشرة المرأة في رياضة البريدج (الاتحاد الدولي WBF)',
        'desc_en': 'Official World Bridge Federation publication on female athletes, teams, and international initiatives.',
        'desc_ar': 'النشرة الرسمية الصادرة عن الاتحاد العالمي للبريدج لدعم وتطوير اللاعبات والناشئات.',
        'filename': 'WBF Women.pdf',
        'filetype': 'PDF',
        'filesize': '2.6 MB',
        'date': '2025-09-01',
        'year': 2025,
        'date_display_en': 'Sep 2025',
        'date_display_ar': 'سبتمبر 2025',
        'icon': 'heart'
    },
    {
        'id': 'jordan_cup_2025_final',
        'category': 'tournaments',
        'title_en': 'Jordan Cup 2025 - Final Standings & VP Matrix',
        'title_ar': 'كأس الأردن 2025 - النتائج النهائية ومصفوفة VP',
        'desc_en': 'Full final results, team VP ranks, and complete head-to-head calculations for Jordan Cup 2025.',
        'desc_ar': 'الترتيب النهائي لبطولة كأس الأردن 2025 ونتائج الجولات ومصفوفة النقاط الكاملة.',
        'filename': 'Jordan Cups 2025 Final.xlsx',
        'filetype': 'XLSX',
        'filesize': '96 KB',
        'date': '2025-04-15',
        'year': 2025,
        'date_display_en': 'Apr 2025',
        'date_display_ar': 'أبريل 2025',
        'icon': 'table'
    },
    {
        'id': 'jordan_cup_2025_r11',
        'category': 'tournaments',
        'title_en': 'Jordan Cup 2025 - Standings After Round 11',
        'title_ar': 'كأس الأردن 2025 - ترتيب الفرق بعد الجولة 11',
        'desc_en': 'Intermediate standings and cumulative VP points after Round 11 of the 2025 season.',
        'desc_ar': 'الترتيب التراكمي ونقاط الفرق بعد انتهاء الجولة 11 من بطولة كأس الأردن 2025.',
        'filename': 'JORDAN CUP 2025 AFTER ROUND 11.xlsx',
        'filetype': 'XLSX',
        'filesize': '96 KB',
        'date': '2025-03-20',
        'year': 2025,
        'date_display_en': 'Mar 2025',
        'date_display_ar': 'مارس 2025',
        'icon': 'file-spreadsheet'
    },
    {
        'id': 'mixed_selection_2025',
        'category': 'tournaments',
        'title_en': 'Jordan National Mixed Selection 2025 - Final VP',
        'title_ar': 'تصفيات المنتخب الأردني للزوجي المختلط 2025 - الترتيب النهائي',
        'desc_en': 'Official VP rankings of Jordan pairs competing for the national mixed team representation.',
        'desc_ar': 'الترتيب النهائي لنقاط VP لفرق الزوجي المختلط المتنافسة لتمثيل المنتخب الوطني 2025.',
        'filename': 'MIX SELECTION FINAL.xlsx',
        'filetype': 'XLSX',
        'filesize': '108 KB',
        'date': '2025-02-10',
        'year': 2025,
        'date_display_en': 'Feb 2025',
        'date_display_ar': 'فبراير 2025',
        'icon': 'award'
    },
    # 2024
    {
        'id': 'festival_2024_prog',
        'category': 'festival',
        'title_en': '41st Jordan International Bridge Festival 2024 - Official Program',
        'title_ar': 'برنامج مهرجان الأردن الدولي الحادي والأربعين 2024',
        'desc_en': 'Official brochure, event regulations, tournament schedule, and venue details for the 41st festival.',
        'desc_ar': 'برنامج وكتيب فعاليات المهرجان الدولي الحادي والأربعين في عمّان ولوائح المنافسات.',
        'filename': 'festival 2024 new.pdf',
        'filetype': 'PDF',
        'filesize': '300 KB',
        'date': '2024-05-10',
        'year': 2024,
        'date_display_en': 'May 2024',
        'date_display_ar': 'مايو 2024',
        'icon': 'file-text'
    },
    {
        'id': 'general_assembly',
        'category': 'governance',
        'title_en': 'General Assembly Roster & Public Committee (Olympic Registry)',
        'title_ar': 'كشف أعضاء الهيئة العامة ومجلس الإدارة (المعتمد أولمبياً)',
        'desc_en': 'Official registry of the General Assembly and Board submitted to the Jordan Olympic Committee.',
        'desc_ar': 'الكشف الرسمي المعتمد لأسماء أعضاء الهيئة العامة ومجلس الإدارة المرفوع للجنة الأولمبية.',
        'filename': 'name of public commite.docx',
        'filetype': 'DOCX',
        'filesize': '31 KB',
        'date': '2024-01-15',
        'year': 2024,
        'date_display_en': 'Jan 2024',
        'date_display_ar': 'يناير 2024',
        'icon': 'users'
    },
    # 2023
    {
        'id': 'festival_2023_prog',
        'category': 'festival',
        'title_en': '40th Jordan International Bridge Festival 2023 - Official Program',
        'title_ar': 'برنامج مهرجان الأردن الدولي الأربعين 2023',
        'desc_en': 'Official schedule, Dead Sea & Citadel tour programs, and tournament regulations for 2023.',
        'desc_ar': 'الجدول الزمني ومكان الإقامة وبرامج الجولات السياحية وتعليمات البطولة لمهرجان 2023.',
        'filename': 'festival 1 2023.pdf',
        'filetype': 'PDF',
        'filesize': '4.8 MB',
        'date': '2023-02-19',
        'year': 2023,
        'date_display_en': 'Feb 2023',
        'date_display_ar': 'فبراير 2023',
        'icon': 'file-text'
    },
    # 2022
    {
        'id': 'festival_2022_prog',
        'category': 'festival',
        'title_en': '39th Jordan International Bridge Festival 2022 - Official Program',
        'title_ar': 'كتيب وبرنامج مهرجان الأردن الدولي التاسع والثلاثين 2022',
        'desc_en': 'Complete commemorative booklet and tournament guide for the 2022 international festival held in Amman.',
        'desc_ar': 'الكتيب الرسمي الكامل لفعاليات مهرجان الأردن الدولي لعام 2022 وجدول المنافسات في عمّان.',
        'filename': 'festival 2022.pdf',
        'filetype': 'PDF',
        'filesize': '5.8 MB',
        'date': '2022-06-29',
        'year': 2022,
        'date_display_en': 'Jun 2022',
        'date_display_ar': 'يونيو 2022',
        'icon': 'file-text'
    },
    # 2021
    {
        'id': 'bylaws_ar',
        'category': 'governance',
        'title_en': 'Official Arabic Constitution (Jordan Olympic Committee Certified)',
        'title_ar': 'النظام الأساسي المعتمد من اللجنة الأولمبية الأردنية (2021)',
        'desc_en': 'Official Arabic statute certified by the Jordan Olympic Committee pursuant to Sports Law No. 73 of 2021.',
        'desc_ar': 'النظام الأساسي المعتمد رسمياً والصادر بموجب نظام الاتحادات الرياضية الأردنية رقم 73 لسنة 2021.',
        'filename': '157516041606159215751605 1575160415751587157515871610 1604160415751578158115751583 1575160415751585158316061610 1604160415761585161015831580 1575160416061607157515741610 2021.pdf',
        'filetype': 'PDF',
        'filesize': '967 KB',
        'date': '2021-09-01',
        'year': 2021,
        'date_display_en': 'Sep 2021',
        'date_display_ar': 'سبتمبر 2021',
        'icon': 'award'
    },
    {
        'id': 'bylaws_en',
        'category': 'governance',
        'title_en': 'By-Laws Jordan Bridge Federation (English Governance)',
        'title_ar': 'النظام الأساسي للاتحاد الأردني للبريدج (النسخة الإنجليزية)',
        'desc_en': 'Official English constitution, governance structure, and federation bylaws issued pursuant to Regulation No. 73.',
        'desc_ar': 'النظام الأساسي الرسمي باللغة الإنجليزية، هيكلية الإدارة ولائحة الاتحاد الصادرة بموجب النظام 73.',
        'filename': 'By-Laws Jordan Bridge Federation KP 220821.pdf',
        'filetype': 'PDF',
        'filesize': '912 KB',
        'date': '2021-08-22',
        'year': 2021,
        'date_display_en': 'Aug 2021',
        'date_display_ar': 'أغسطس 2021',
        'icon': 'scroll-text'
    },
    # 2019 (BFAME Amman Daily Bulletins)
    {
        'id': 'bulletin_4',
        'category': 'bulletins',
        'title_en': '20th BFAME Amman - Daily Bulletin #4 (Championship Special)',
        'title_ar': 'بطولة BFAME العشرون في عمان - النشرة اليومية 4 (الختامي)',
        'desc_en': 'Finals scorecards, podium winners, gala dinner photos, and closing ceremony coverage.',
        'desc_ar': 'نتائج النهائي، تتويج الأبطال، صور الحفل الختامي وتوزيع الجوائز لبطولة آسيا والشرق الأوسط.',
        'filename': 'Bulletin-4.pdf',
        'filetype': 'PDF',
        'filesize': '1.6 MB',
        'date': '2019-06-27',
        'year': 2019,
        'date_display_en': '27 Jun 2019',
        'date_display_ar': '27 يونيو 2019',
        'icon': 'newspaper'
    },
    {
        'id': 'bulletin_3',
        'category': 'bulletins',
        'title_en': '20th BFAME Amman - Daily Bulletin #3',
        'title_ar': 'بطولة BFAME العشرون في عمان - النشرة اليومية 3',
        'desc_en': 'Semi-final clashes, Butler rankings, Executive Council elections, and tournament human interest stories.',
        'desc_ar': 'منافسات نصف النهائي، ترتيب البتلر، انتخابات المجلس التنفيذي وقصص وحوارات البطولة.',
        'filename': 'Bulletin-3.pdf',
        'filetype': 'PDF',
        'filesize': '1.6 MB',
        'date': '2019-06-26',
        'year': 2019,
        'date_display_en': '26 Jun 2019',
        'date_display_ar': '26 يونيو 2019',
        'icon': 'newspaper'
    },
    {
        'id': 'bulletin_2',
        'category': 'bulletins',
        'title_en': '20th BFAME Amman - Daily Bulletin #2',
        'title_ar': 'بطولة BFAME العشرون في عمان - النشرة اليومية 2',
        'desc_en': 'Round 1-3 results, masterpoint leaderboards, guest honor profile, and expert bidding analysis.',
        'desc_ar': 'نتائج الجولات الأولى، ترتيب النقاط، وكلمة ضيف الشرف وتحليلات فنية للمزايدات.',
        'filename': 'Bulletin-2.pdf',
        'filetype': 'PDF',
        'filesize': '2.6 MB',
        'date': '2019-06-25',
        'year': 2019,
        'date_display_en': '25 Jun 2019',
        'date_display_ar': '25 يونيو 2019',
        'icon': 'newspaper'
    },
    {
        'id': 'bulletin_1',
        'category': 'bulletins',
        'title_en': '20th BFAME Amman - Daily Bulletin #1',
        'title_ar': 'بطولة BFAME العشرون في عمان - النشرة اليومية 1',
        'desc_en': 'Welcome message, opening ceremony coverage, team line-ups, and daily hand commentary.',
        'desc_ar': 'كلمة الترحيب، حفل الافتتاح، تشكيلة الفرق وتحليل التوزيعات اليومية للبطولة.',
        'filename': 'Bulletin-1.pdf',
        'filetype': 'PDF',
        'filesize': '2.7 MB',
        'date': '2019-06-24',
        'year': 2019,
        'date_display_en': '24 Jun 2019',
        'date_display_ar': '24 يونيو 2019',
        'icon': 'newspaper'
    },
    {
        'id': 'pre_bulletin',
        'category': 'bulletins',
        'title_en': '20th BFAME Amman - Pre-Championship Bulletin',
        'title_ar': 'بطولة BFAME العشرون في عمان - النشرة التمهيدية',
        'desc_en': 'Official welcome to Amman, participating nations, championship schedule, and technical regulations.',
        'desc_ar': 'الترحيب بالوفود في عمان، الدول المشاركة، جدول المنافسات واللوائح الفنية لبطولة آسيا والشرق الأوسط.',
        'filename': 'Pre_Bulletin.pdf',
        'filetype': 'PDF',
        'filesize': '1.4 MB',
        'date': '2019-06-23',
        'year': 2019,
        'date_display_en': '23 Jun 2019',
        'date_display_ar': '23 يونيو 2019',
        'icon': 'newspaper'
    },
    # Standing / Historical
    {
        'id': 'annual_festival_doc',
        'category': 'festival',
        'title_en': 'Annual Jordan International Festival Prospectus',
        'title_ar': 'دليل ونظام مهرجان الأردن الدولي السنوي',
        'desc_en': 'Complete history, tournament format, and event organization standards for the annual festival.',
        'desc_ar': 'تاريخ المهرجان، نظام المنافسات، والمعايير التنظيمية للحدث السنوي العريق.',
        'filename': 'Annual Jordan International Bridge Festival.docx',
        'filetype': 'DOCX',
        'filesize': '341 KB',
        'date': '2018-05-01',
        'year': 2018,
        'date_display_en': 'Standing Guide',
        'date_display_ar': 'دليل معتمد',
        'icon': 'book-open'
    },
    {
        'id': 'bfame_records',
        'category': 'international',
        'title_en': 'BFAME Historical Participation & Championship Records',
        'title_ar': 'سجل مشاركات وإنجازات الأردن التاريخية في BFAME',
        'desc_en': 'Official records of Jordan national teams in BFAME championships from 1981 to 2017.',
        'desc_ar': 'سجل مشاركات ونتائج منتخبات الأردن في بطولات آسيا والشرق الأوسط للبريدج من 1981 حتى 2017.',
        'filename': 'BFAME Participation Record.pdf',
        'filetype': 'PDF',
        'filesize': '40 KB',
        'date': '2017-03-14',
        'year': 2017,
        'date_display_en': '1981–2017 Archive',
        'date_display_ar': 'أرشيف 1981–2017',
        'icon': 'globe'
    },
    {
        'id': 'wbf_alerting',
        'category': 'international',
        'title_en': 'WBF Official Alerting Policy',
        'title_ar': 'سياسة التنبيه المعتمدة من الاتحاد الدولي (WBF)',
        'desc_en': 'World Bridge Federation regulations for bidding alerts, announcements, and screens.',
        'desc_ar': 'تعليمات وسياسة التنبيهات الرسمية للإعلانات والمزايدة والشاشات من الاتحاد العالمي للبريدج.',
        'filename': 'WBF Alerting Policy.pdf',
        'filetype': 'PDF',
        'filesize': '44 KB',
        'date': '2011-07-08',
        'year': 2011,
        'date_display_en': 'Standing Policy',
        'date_display_ar': 'لائحة معتمدة',
        'icon': 'bell'
    }
]

master_data = {
    'historicalFestivals': festivals,
    'jordanCup2026': {
        'tournament': 'Jordan Cup 2026 Final',
        'director': 'Raad Otoom',
        'matrix': matrix_2026,
        'schedule': schedule_2026
    },
    'jordanCup2025': {
        'tournament': 'Jordan Cup 2025 Final',
        'director': 'Raad Otoom',
        'matrix': matrix_2025
    },
    'mixSelection2025': {
        'tournament': 'National Mixed Selection League 2025',
        'pairs': mix_pairs
    },
    'documents': docs_inventory
}

output_path = os.path.join(data_dir, 'jbf_master_data.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(master_data, f, ensure_ascii=False, indent=2)

print(f"SUCCESS: Saved comprehensive master data to {output_path}")
