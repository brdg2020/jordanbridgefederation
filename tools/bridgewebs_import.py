# -*- coding: utf-8 -*-
"""Convert the captured JBF Bridgewebs results archive into site JSON.

Input : tools/bridgewebs_raw.json.gz  (raw XML/HTML responses captured from
        https://www.bridgewebs.com/cgi-bin/bwor/bw.cgi?club=jbf&pid=display_past,
        one entry per event: ranking, scorecard/traveller XML, hands, matches)
Output: public/data/results/index.json and public/data/results/events/<event>.json

Nothing is computed or invented here: every value is copied from the Bridgewebs
responses. Requires beautifulsoup4.
"""
import json,re,html,os,collections
from bs4 import BeautifulSoup
def res(x,tag='results'):
    m=re.search(r'<%s>(.*?)</%s>'%(tag,tag),x or '',re.S); return html.unescape(m.group(1)) if m else ''
import gzip,sys
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(BASE,'tools','bridgewebs_raw.json.gz')
OUT=os.path.join(BASE,'public','data','results')
d=json.load(gzip.open(RAW,'rt',encoding='utf-8'))
SEATS='NESW'
DLR={'1':'N','2':'E','3':'S','4':'W'}
VUL={'1':'None','2':'NS','3':'EW','4':'All'}

def clean(s): return re.sub(r'[ \t\r\f\v\xa0]+',' ',s).strip()

def cell_text(td):
    divs=td.find_all('div',recursive=False)
    if len(divs)>1: return '\n'.join(clean(x.get_text(' ')) for x in divs)
    # replace suit images with letters
    for img in td.find_all('img'):
        alt=(img.get('alt') or '').lower()
        img.replace_with({'spade':'♠','heart':'♥','diamond':'♦','club':'♣'}.get(alt,''))
    for br in td.find_all('br'): br.replace_with('\n')
    return '\n'.join(clean(x) for x in td.get_text().split('\n') if clean(x))

def parse_table(t):
    rows=[]
    for tr in t.find_all('tr'):
        if tr.find_parent('table') is not t: continue
        cells=[]
        for td in tr.find_all(['td','th'],recursive=False):
            c={'t':cell_text(td)}
            cs=int(td.get('colspan',1) or 1); rs=int(td.get('rowspan',1) or 1)
            if cs>1: c['cs']=cs
            if rs>1: c['rs']=rs
            if 'brx_title' in (td.get('class') or []) or 'brx_title_s' in (td.get('class') or []): c['h']=1
            cells.append(c)
        if cells and any(c['t'] for c in cells): rows.append(cells)
    return rows

def parse_rank(xml):
    h=res(xml); s=BeautifulSoup(h,'html.parser')
    tables=[]; info=[]
    for t in s.find_all('table',class_='brx_table'):
        if t.find_parent('table',class_='brx_table'): continue
        tables.append(parse_table(t))
    # key/value footer
    for tr in s.find_all('tr'):
        tds=tr.find_all('td',recursive=False)
        if len(tds)==3 and clean(tds[1].get_text())==':' and not tr.find_parent('table',class_='brx_table'):
            info.append([clean(tds[0].get_text()),clean(tds[2].get_text())])
    # notes / free text outside tables (e.g. headers)
    return {'tables':tables,'info':info}

def parse_alltravs(xml):
    m=re.search(r'<alltravs>(.*)</alltravs>',xml or '',re.S)
    if not m: return None
    pages=re.findall(r'<page>(.*?)</page>',m.group(1),re.S)
    def f(pg,tag):
        x=re.search(r'<%s>(.*?)</%s>'%(tag,tag),pg,re.S); return html.unescape(x.group(1)) if x else None
    pairs=[];boards=[]
    for pg in pages:
        v=f(pg,'view')
        if v=='6':
            for rw in re.findall(r'<rw>(.*?)</rw>',pg,re.S):
                p=html.unescape(rw).split(';')
                pairs.append({'no':p[2],'way':p[1],'pair':p[3],'names':[clean(p[4]),clean(p[5])],'team':p[6] if len(p)>6 else ''})
        elif f(pg,'bd') is not None:
            hand=(f(pg,'hand') or '').split(';')
            b={'bd':f(pg,'bd'),'sess':f(pg,'sess'),'title':clean(f(pg,'title') or ''),'dealer':DLR.get(f(pg,'dlr') or '',''),'vul':VUL.get(f(pg,'vul') or '','')}
            if len(hand)>=16 and any(x for x in hand[:16]):
                b['hands']={SEATS[i]:[('' if hand[i*4+j]=='--' else hand[i*4+j]) for j in range(4)] for i in range(4)}
                hcp=hand[16:20]
                if any(hcp): b['hcp']=dict(zip(SEATS,hcp))
                mk=hand[20:40]
                if len(mk)==20 and any(x for x in mk):
                    # bridgewebs order: players N,S,E,W ; each C,D,H,S,NT (tricks)
                    dd={}
                    for pi,pl in enumerate('NSEW'):
                        blk=mk[pi*5:pi*5+5]; dd[pl]=dict(zip(['C','D','H','S','NT'],blk))
                    b['dd']=dd
            com=clean(re.sub('<[^>]+>',' ',f(pg,'commentary') or ''))
            if com: b['commentary']=com
            c1=f(pg,'cols1')
            if c1: b['groups']=[[x.split(',')[0],int(x.split(',')[1])] for x in c1.split(';') if ',' in x]
            b['cols']=(f(pg,'cols') or '').split(';')
            b['rows']=[html.unescape(r).split(';') for r in re.findall(r'<rw>(.*?)</rw>',pg,re.S)]
            boards.append(b)
    return {'pairs':pairs,'boards':boards}

def parse_show_hands(xml):
    h=res(xml); s=BeautifulSoup(h,'html.parser'); boards=[]
    for o in s.find_all('div',class_='houter'):
        bn=o.find(class_='hbdno')
        if not bn: continue
        b={'bd':clean(bn.get_text())}
        for tr in o.find_all('tr'):
            tds=tr.find_all('td',class_='htext')
            if len(tds)==2:
                k=clean(tds[0].get_text()).rstrip(':'); v=clean(tds[1].get_text())
                if k=='Dlr': b['dealer']={'North':'N','East':'E','South':'S','West':'W'}.get(v,v)
                if k=='Vul': b['vul']={'None':'None','N/S':'NS','E/W':'EW','All':'All','Both':'All'}.get(v,v)
        hh=o.find_all('table',class_='hht')
        if len(hh)==4:
            order=['N','W','E','S']; hands={}
            for seat,t in zip(order,hh):
                suits=[clean(td.get_text()).replace('10','T') for td in t.find_all('td',class_='hand')]
                hands[seat]=[x if x not in('-','--') else '' for x in suits]
            if any(''.join(v) for v in hands.values()):
                b['hands']={k:hands[k] for k in 'NESW'}
        hc=[clean(x.get_text()) for x in o.find_all('td',class_='hhcp')]
        if len(hc)==4 and any(hc): b['hcp']={'N':hc[0],'W':hc[1],'E':hc[2],'S':hc[3]}
        mk={}
        for tr in o.find_all('tr'):
            p=tr.find('td',class_='hmakep')
            if p:
                vals=[clean(x.get_text()) for x in tr.find_all('td',class_='hmake')]
                mk[clean(p.get_text())]=vals
        if mk: b['ddl']={k:dict(zip(['C','D','H','S','NT'],v)) for k,v in mk.items()}
        boards.append(b)
    return boards

def table_pages(xml):
    h=res(xml); s=BeautifulSoup(h,'html.parser'); out=[]
    for t in s.find_all('table',class_='brx_table'):
        if t.find_parent('table',class_='brx_table'): continue
        out.append(parse_table(t))
    return out

def match_page(xml):
    h=res(xml); s=BeautifulSoup(h,'html.parser')
    cur=s.find(class_='xoptcurrent'); team=clean(cur.get_text()) if cur else ''
    tabs=table_pages(xml)
    # meaningful if any board row has a real contract/score
    has=False
    for t in tabs:
        for r in t:
            vals=[c['t'] for c in r if not c.get('h')]
            if vals and re.match(r'^\d+$',vals[0] or '') and any(re.match(r'^[1-7](NT|[SHDC])|^Pass|^-?\d{2,4}$',v) for v in vals[1:] if v not in('0',)):
                has=True
    return team,tabs,has

def classify(title,heads):
    t=title.lower()
    if 'festival' in t: cat='Jordan Bridge Festival'
    elif 'jordan cup' in t: cat="Jordan Cup"
    elif 'selection' in t or 'qulification' in t or 'qualification' in t: cat='Selection & Qualification'
    else: cat='Other Events'
    H=' '.join(heads).lower()
    if 'butler' in H: typ='Butler Pairs'
    elif 'vps' in H or 'imps' in H or 'team' in H: typ='Teams'
    else: typ='Pairs'
    return cat,typ

events=[]; os.makedirs(os.path.join(OUT,'events'),exist_ok=True)
MON={m:i for i,m in enumerate(['January','February','March','April','May','June','July','August','September','October','November','December'],1)}
for ek,o in d.items():
    title_html=o['title']; parts=[clean(BeautifulSoup(x,'html.parser').get_text()) for x in re.split(r'<br\s*/?>',title_html)]
    full=' - '.join(parts)
    # strip leading date
    name=re.sub(r'^\d{1,2}(st|nd|rd|th) \w+ \d{4}( - )?','',full).strip()
    date=f'{ek[:4]}-{ek[4:6]}-{ek[6:8]}'
    label=o['meta']['label'].split('\n')[0].replace('\xa0',' ').strip()
    tables_m=re.search(r'\(([\d½]+) tables?\)',label)
    staff=[clean(x) for x in (o['meta']['staff'] or '').split('\n') if clean(x)]
    ms=[m[0] for m in o['msecs']] or ['']
    sections=[]
    for i,m in enumerate(ms):
        sec={'label': o['msecs'][i][1] if o['msecs'] else ''}
        sec['ranking']=parse_rank(o['pages']['rank_'+m])
        at=parse_alltravs(o['pages'].get('sc_'+m))
        if at:
            sec['pairs']=at['pairs']
            if at['boards']: sec['boards']=at['boards']
        if not sec.get('boards') and o['pages'].get('hands_'+m):
            # no traveller data for this section: use the hand records page
            hb=[b for b in parse_show_hands(o['pages']['hands_'+m]) if b.get('hands')]
            if hb: sec['boards']=hb
        mt=[]
        for p in sorted([p for p in o['pages'] if p.startswith('match_'+m+'_')],key=lambda x:int(x.split('_')[-1])):
            team,tabs,has=match_page(o['pages'][p])
            if has: mt.append({'team':team,'tables':tabs})
        if mt: sec['matches']=mt
        if o['pages'].get('ximps_'+m):
            x=table_pages(o['pages']['ximps_'+m])
            if x: sec['ximps']=x
        if o['pages'].get('extra_'+m):
            h=res(o['pages']['extra_'+m]); s=BeautifulSoup(h,'html.parser')
            txt=clean(s.get_text(' '))
            x=table_pages(o['pages']['extra_'+m])
            sec['information']={'tables':x,'text':txt if not x else ''}
        sections.append(sec)
    heads=[c['t'] for t in sections[0]['ranking']['tables'][:1] for r in t[:1] for c in r]
    cat,typ=classify(name,heads)
    ev={'id':ek,'date':date,'year':int(ek[:4]),'title':name,'category':cat,'type':typ,
        'tables':tables_m.group(1) if tables_m else '','staff':staff,
        'source':f'https://www.bridgewebs.com/cgi-bin/bwor/bw.cgi?pid=display_rank&event={ek}&club=jbf',
        'sections':sections}
    json.dump(ev,open(os.path.join(OUT,'events',ek+'.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    nb=sum(len(s.get('boards',[])) for s in sections)
    nh=sum(1 for s in sections for b in s.get('boards',[]) if b.get('hands'))
    nt=sum(1 for s in sections for b in s.get('boards',[]) if b.get('rows'))
    events.append({'id':ek,'date':date,'year':ev['year'],'title':name,'category':cat,'type':typ,'tables':ev['tables'],'staff':staff,
                   'sections':[s['label'] for s in sections if s['label']],'boards':nb,'hands':nh>0,'travellers':nt>0,'matches':any(s.get('matches') for s in sections)})
events.sort(key=lambda e:(e['date'],e['id']),reverse=True)
json.dump({'source':'https://www.bridgewebs.com/cgi-bin/bwor/bw.cgi?club=jbf&pid=display_past','events':events},open(os.path.join(OUT,'index.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(f'{len(events)} events written to {OUT}')
