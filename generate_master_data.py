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
    'Alfa': ['Randa Al Saket', 'Azza Qudah', 'Hala Sawaf', 'Amal Fakhouri'],
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

# Schedule 2026
sched_file = os.path.join(archive_dir, 'Jordan Cups 26 schedule.xlsx')
wb_sched = openpyxl.load_workbook(sched_file, data_only=True)
ws_sched = wb_sched.active
schedule_2026 = []
# Matches are in rows 18-24, columns
current_round = None
round_matches = []
for r in range(16, 45):
    val_a = ws_sched.cell(r, 1).value
    val_b = ws_sched.cell(r, 2).value
    val_c = ws_sched.cell(r, 3).value
    val_d = ws_sched.cell(r, 4).value
    text = " ".join([str(x) for x in [val_a, val_b, val_c, val_d] if x])
    if 'Round' in text:
        if current_round is not None and round_matches:
            schedule_2026.append({'round': current_round, 'matches': round_matches})
            round_matches = []
        m = re.search(r'Round\s*#?\s*0?(\d+)', text, re.IGNORECASE)
        current_round = int(m.group(1)) if m else len(schedule_2026) + 1
    elif val_a and val_d and ('-' in str(val_b) or '-' in str(val_c) or val_a != 'Home'):
        h = str(val_a).strip()
        a = str(val_d).strip()
        if h and a and h != 'Teams' and a != 'Teams':
            round_matches.append({'home': h, 'away': a})

if current_round is not None and round_matches:
    schedule_2026.append({'round': current_round, 'matches': round_matches})

# Fallback schedule if empty
if not schedule_2026:
    schedule_2026 = [
        {'round': 1, 'matches': [{'home': 'Lions', 'away': 'Eagles'}, {'home': 'Jordan Teams', 'away': 'Palestine'}, {'home': 'Ortho Group', 'away': 'AL Nashama'}, {'home': 'Jordan Mix', 'away': 'Alfa'}]},
        {'round': 2, 'matches': [{'home': 'Eagles', 'away': 'AL Nashama'}, {'home': 'Alfa', 'away': 'Ortho Group'}, {'home': 'Jordan Teams', 'away': 'Jordan Mix'}, {'home': 'Palestine', 'away': 'Lions'}]},
        {'round': 3, 'matches': [{'home': 'Jordan Mix', 'away': 'Palestine'}, {'round': 3, 'home': 'AL Nashama', 'away': 'Alfa'}, {'home': 'Lions', 'away': 'Jordan Teams'}, {'home': 'Ortho Group', 'away': 'Eagles'}]},
        {'round': 4, 'matches': [{'home': 'Palestine', 'away': 'Ortho Group'}, {'home': 'Jordan Teams', 'away': 'AL Nashama'}, {'home': 'Alfa', 'away': 'Eagles'}, {'home': 'Jordan Mix', 'away': 'Lions'}]},
        {'round': 5, 'matches': [{'home': 'Eagles', 'away': 'Jordan Teams'}, {'home': 'Lions', 'away': 'Alfa'}, {'home': 'Ortho Group', 'away': 'Jordan Mix'}, {'home': 'AL Nashama', 'away': 'Palestine'}]},
        {'round': 6, 'matches': [{'home': 'Palestine', 'away': 'Alfa'}, {'home': 'Jordan Mix', 'away': 'Eagles'}, {'home': 'Lions', 'away': 'AL Nashama'}, {'home': 'Jordan Teams', 'away': 'Ortho Group'}]},
        {'round': 7, 'matches': [{'home': 'AL Nashama', 'away': 'Jordan Mix'}, {'home': 'Eagles', 'away': 'Palestine'}, {'home': 'Alfa', 'away': 'Jordan Teams'}, {'home': 'Ortho Group', 'away': 'Lions'}]}
    ]

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
mix_file = os.path.join(archive_dir, 'MIX SELECTION FINAL.xlsx')
wb_mix = openpyxl.load_workbook(mix_file, data_only=True)
ws_mix = wb_mix['Sheet1'] if 'Sheet1' in wb_mix.sheetnames else wb_mix.active

mix_pairs = []
for r in range(3, 10):
    pname = ws_mix.cell(r, 1).value
    if not pname:
        continue
    pname = str(pname).strip()
    r_scores = []
    # 5 rounds
    for rnd in range(1, 6):
        c_imp = 2 + (rnd - 1) * 2
        c_vp = c_imp + 1
        imp_v = ws_mix.cell(r, c_imp).value
        vp_v = ws_mix.cell(r, c_vp).value
        r_scores.append({
            'round': rnd,
            'imp': int(float(imp_v)) if imp_v is not None else 0,
            'vp': round(float(vp_v), 2) if vp_v is not None else 0.0
        })
    tot_imp = ws_mix.cell(r, 12).value
    tot_vp = ws_mix.cell(r, 13).value
    
    mix_pairs.append({
        'pair': pname,
        'rounds': r_scores,
        'totalImp': int(float(tot_imp)) if tot_imp is not None else 0,
        'totalVp': round(float(tot_vp), 2) if tot_vp is not None else 0.0
    })

mix_pairs.sort(key=lambda x: x['totalVp'], reverse=True)
for idx, p in enumerate(mix_pairs):
    p['rank'] = idx + 1

# 5. Documents Inventory
docs_inventory = [
    {
        'id': 'bylaws_en',
        'category': 'governance',
        'title_en': 'By-Laws Jordan Bridge Federation',
        'title_ar': 'النظام الأساسي للاتحاد الأردني للبريدج',
        'desc_en': 'Official English constitution, governance structure, and federation bylaws.',
        'desc_ar': 'النظام الأساسي الرسمي باللغة الإنجليزية، هيكلية الإدارة ولائحة الاتحاد.',
        'filename': 'By-Laws Jordan Bridge Federation KP 220821.pdf',
        'filetype': 'PDF',
        'filesize': '912 KB',
        'icon': 'scroll-text'
    },
    {
        'id': 'bylaws_ar',
        'category': 'governance',
        'title_en': 'Official Arabic Constitution (Olympic Committee Approved)',
        'title_ar': 'النظام الأساسي المعتمد من اللجنة الأولمبية الأردنية',
        'desc_en': 'Official Arabic statute certified by the Jordan Olympic Committee (2021).',
        'desc_ar': 'النظام الأساسي المعتمد رسمياً والصادر عن اللجنة الأولمبية الأردنية (2021).',
        'filename': '157516041606159215751605 1575160415751587157515871610 1604160415751578158115751583 1575160415751585158316061610 1604160415761585161015831580 1575160416061607157515741610 2021.pdf',
        'filetype': 'PDF',
        'filesize': '967 KB',
        'icon': 'award'
    },
    {
        'id': 'wbf_alerting',
        'category': 'regulations',
        'title_en': 'WBF Official Alerting Policy',
        'title_ar': 'سياسة التنبيه المعتمدة من الاتحاد الدولي (WBF)',
        'desc_en': 'World Bridge Federation regulations for bidding alerts, announcements, and screens.',
        'desc_ar': 'تعليمات وسياسة التنبيهات الرسمية للإعلانات والمزايدة والشاشات من الاتحاد العالمي.',
        'filename': 'WBF Alerting Policy.pdf',
        'filetype': 'PDF',
        'filesize': '44 KB',
        'icon': 'bell'
    },
    {
        'id': 'bfame_records',
        'category': 'international',
        'title_en': 'BFAME Participation & Historical Record',
        'title_ar': 'سجل مشاركات وإنجازات الأردن في BFAME',
        'desc_en': 'Official records of Jordan national teams in the Bridge Federation of Asia & Middle East.',
        'desc_ar': 'سجل مشاركات ونتائج منتخبات الأردن في بطولات اتحاد آسيا والشرق الأوسط للبريدج.',
        'filename': 'BFAME Participation Record.pdf',
        'filetype': 'PDF',
        'filesize': '40 KB',
        'icon': 'globe'
    },
    {
        'id': 'wbf_women',
        'category': 'international',
        'title_en': 'WBF Women in Bridge Programme',
        'title_ar': 'برنامج المرأة في رياضة البريدج (WBF)',
        'desc_en': 'International initiatives for female bridge athletes and junior development.',
        'desc_ar': 'المبادرات الدولية لدعم وتطوير اللاعبات السيدات والناشئات في رياضة البريدج.',
        'filename': 'WBF Women.pdf',
        'filetype': 'PDF',
        'filesize': '2.6 MB',
        'icon': 'heart'
    },
    {
        'id': 'general_assembly',
        'category': 'governance',
        'title_en': 'General Assembly Roster & Public Committee',
        'title_ar': 'كشف أعضاء الهيئة العامة للاتحاد',
        'desc_en': 'Official registry of the General Assembly submitted to the Jordan Olympic Committee.',
        'desc_ar': 'الكشف الرسمي المعتمد لأسماء أعضاء الهيئة العامة المرفوع للجنة الأولمبية.',
        'filename': 'name of public commite.docx',
        'filetype': 'DOCX',
        'filesize': '31 KB',
        'icon': 'users'
    },
    {
        'id': 'annual_festival_doc',
        'category': 'festival',
        'title_en': 'Annual Jordan International Festival Prospectus',
        'title_ar': 'دليل ونظام مهرجان الأردن الدولي السنوي',
        'desc_en': 'Complete history, tournament format, and event organization standards.',
        'desc_ar': 'تاريخ المهرجان، نظام المنافسات، والمعايير التنظيمية للحدث السنوي العريق.',
        'filename': 'Annual Jordan International Bridge Festival.docx',
        'filetype': 'DOCX',
        'filesize': '341 KB',
        'icon': 'book-open'
    },
    {
        'id': 'bulletin_1',
        'category': 'bulletins',
        'title_en': 'Festival Daily Bulletin #1',
        'title_ar': 'النشرة اليومية للمهرجان - العدد 1',
        'desc_en': 'Welcome message, opening ceremony coverage, team line-ups, and daily hands.',
        'desc_ar': 'كلمة الترحيب، حفل الافتتاح، تشكيلة الفرق، وتحليل التوزيعات اليومية.',
        'filename': 'Bulletin-1.pdf',
        'filetype': 'PDF',
        'filesize': '2.7 MB',
        'icon': 'newspaper'
    },
    {
        'id': 'bulletin_2',
        'category': 'bulletins',
        'title_en': 'Festival Daily Bulletin #2',
        'title_ar': 'النشرة اليومية للمهرجان - العدد 2',
        'desc_en': 'Round 1-3 results, masterpoint leaderboards, and expert bidding analysis.',
        'desc_ar': 'نتائج الجولات الأولى وترتيب النقاط وتحليل فني لمزايدات وألعاب مميزة.',
        'filename': 'Bulletin-2.pdf',
        'filetype': 'PDF',
        'filesize': '2.6 MB',
        'icon': 'newspaper'
    },
    {
        'id': 'bulletin_3',
        'category': 'bulletins',
        'title_en': 'Festival Daily Bulletin #3',
        'title_ar': 'النشرة اليومية للمهرجان - العدد 3',
        'desc_en': 'Semi-final clashes, Butler rankings, and tournament human interest stories.',
        'desc_ar': 'منافسات نصف النهائي، ترتيب البتلر، وقصص وحوارات مع نجوم البطولة.',
        'filename': 'Bulletin-3.pdf',
        'filetype': 'PDF',
        'filesize': '1.6 MB',
        'icon': 'newspaper'
    },
    {
        'id': 'bulletin_4',
        'category': 'bulletins',
        'title_en': 'Festival Daily Bulletin #4 (Championship Special)',
        'title_ar': 'النشرة اليومية للمهرجان - العدد 4 (الختامي)',
        'desc_en': 'Finals scorecards, podium winners, gala dinner photos, and closing speech.',
        'desc_ar': 'نتائج النهائي، تتويج الأبطال، صور الحفل الختامي وتوزيع الجوائز.',
        'filename': 'Bulletin-4.pdf',
        'filetype': 'PDF',
        'filesize': '1.6 MB',
        'icon': 'newspaper'
    },
    {
        'id': 'festival_2022_prog',
        'category': 'festival',
        'title_en': 'Jordan Bridge Festival 2022 Official Program',
        'title_ar': 'كتيب وبرنامج مهرجان الأردن للبريدج 2022',
        'desc_en': 'Complete booklet for the 2022 international festival held in Amman.',
        'desc_ar': 'الكتيب الرسمي الكامل لفعاليات مهرجان الأردن الدولي لعام 2022 في عمّان.',
        'filename': 'festival 2022.pdf',
        'filetype': 'PDF',
        'filesize': '5.7 MB',
        'icon': 'file-text'
    },
    {
        'id': 'festival_2023_prog',
        'category': 'festival',
        'title_en': 'Jordan Bridge Festival 2023 Official Program',
        'title_ar': 'كتيب وبرنامج مهرجان الأردن للبريدج 2023',
        'desc_en': 'Schedule, venue details, and tournament guidelines for the 2023 festival.',
        'desc_ar': 'الجدول الزمني ومكان الإقامة وتعليمات البطولة لمهرجان 2023.',
        'filename': 'festival 1 2023.pdf',
        'filetype': 'PDF',
        'filesize': '4.7 MB',
        'icon': 'file-text'
    },
    {
        'id': 'festival_2024_prog',
        'category': 'festival',
        'title_en': 'Jordan Bridge Festival 2024 Official Program',
        'title_ar': 'برنامج مهرجان الأردن للبريدج 2024',
        'desc_en': 'Program brochure and regulations for the 41st Jordan International Festival.',
        'desc_ar': 'برنامج وكتيب فعاليات المهرجان الدولي الحادي والأربعين في عمّان.',
        'filename': 'festival 2024 new.pdf',
        'filetype': 'PDF',
        'filesize': '300 KB',
        'icon': 'file-text'
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
